import os
import textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips
from agents.script_agent import ShortScript

def create_flowing_text_clip(image_path: str, texts: list[str], duration: float, narration: str = ""):
    """Creates a video clip displaying sequential flowing/typing captions using Pillow."""
    img_base = Image.open(image_path).convert("RGB")

    try:
        # Try to load a sans-serif bold italic font
        font = ImageFont.truetype("arialbi.ttf", 45)
    except IOError:
        try:
            # Fallback to Arial Italic if bold italic isn't available
            font = ImageFont.truetype("ariali.ttf", 45)
        except IOError:
            font = ImageFont.load_default(size=40)

    if not texts:
        texts = [""]
        
    caption_times = []
    
    # Find exactly where each caption occurs in the narration for perfect audio sync
    if narration and texts and texts != [""]:
        narration_clean = narration.lower()
        for p in ".,!?;:\"'":
            narration_clean = narration_clean.replace(p, "")
            
        starts = []
        last_idx = 0
        for text in texts:
            text_clean = text.lower()
            for p in ".,!?;:\"'":
                text_clean = text_clean.replace(p, "")
                
            idx = narration_clean.find(text_clean, last_idx)
            if idx == -1: # Fallback: search from beginning if paraphrased slightly
                idx = narration_clean.find(text_clean)
            if idx == -1: # Fallback: attach it to the end of the previous clip
                idx = last_idx
                
            starts.append(idx)
            last_idx = max(last_idx, idx + len(text_clean))
            
        # Ensure chronological order
        for i in range(1, len(starts)):
            if starts[i] < starts[i-1]:
                starts[i] = starts[i-1]
                
        # Map string indexes to video timestamps
        for i in range(len(texts)):
            start_frac = starts[i] / max(len(narration_clean), 1)
            start_time = duration * start_frac
            caption_times.append([start_time, duration])
            
        # Distribute the end times to make them sequential clips
        for i in range(len(caption_times) - 1):
            if caption_times[i+1][0] <= caption_times[i][0] + 0.1:
                caption_times[i+1][0] = min(caption_times[i][0] + 0.1, duration)
            caption_times[i][1] = caption_times[i+1][0]
            
        caption_times[-1][1] = duration
    else:
        # Fallback to simple proportional time allocation
        total_scene_chars = sum(len(text.strip()) for text in texts)
        current_start_time = 0.0
        for text in texts:
            fraction = len(text.strip()) / total_scene_chars if total_scene_chars > 0 else 1.0 / len(texts)
            cap_duration = duration * fraction
            caption_times.append([current_start_time, current_start_time + cap_duration])
            current_start_time += cap_duration

    def make_frame(t):
        img = img_base.copy()
        draw = ImageDraw.Draw(img)
        
        # Determine which caption should be shown at time 't' based on character proportions
        cap_idx = len(texts) - 1
        for i, (start_time, end_time) in enumerate(caption_times):
            if start_time <= t < end_time:
                cap_idx = i
                break
                
        current_text = texts[cap_idx]
        start_time, end_time = caption_times[cap_idx]
        cap_duration = end_time - start_time
        local_t = t - start_time # Time elapsed for THIS specific caption
        
        wrapped_text = textwrap.wrap(current_text, width=20)
        total_chars = sum(len(line) for line in wrapped_text)
        
        # Pre-calculate heights for centering this specific caption
        total_text_height = 0
        line_heights = []
        for line in wrapped_text:
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_height = line_bbox[3] - line_bbox[1]
            line_heights.append(line_height)
            total_text_height += line_height
            
        start_y = (img.height * 0.75) - (total_text_height / 2)
        
        # Reveal text much faster: max 0.8 seconds, or 80% of its allocated time
        reveal_duration = min(0.8, cap_duration * 0.8)
        if reveal_duration <= 0 or local_t >= reveal_duration or total_chars == 0:
            chars_to_show = total_chars
        else:
            chars_to_show = int((local_t / reveal_duration) * total_chars)
            
        current_y = start_y
        chars_drawn = 0
        
        for i, line in enumerate(wrapped_text):
            if chars_drawn >= chars_to_show:
                break
                
            chars_left = chars_to_show - chars_drawn
            line_to_draw = line[:chars_left]
            chars_drawn += len(line)
            
            # Center based on the FULL line width so text doesn't jump around as it types
            full_line_width = draw.textlength(line, font=font)
            x = (img.width - full_line_width) / 2
            
            draw.text((x, current_y), line_to_draw, font=font, fill="white", stroke_width=5, stroke_fill="black")
            current_y += line_heights[i]
            
        return np.array(img)
        
    return VideoClip(make_frame, duration=duration)

def edit_video(script: ShortScript, image_paths: list[str], audio_paths: list[str], output_dir: str = "output_assets") -> str:
    print("\n--- STITCHING VIDEO TOGETHER ---")

    if not image_paths or not audio_paths or len(image_paths) != len(audio_paths):
        print("Error: Mismatch in number of images and audio files.")
        return ""

    clips = []
    audio_clips = []

    for i, scene in enumerate(script.scenes):
        print(f"Processing scene {scene.scene_number}...")

        # Load the audio to get its exact duration
        audio_clip = AudioFileClip(audio_paths[i])
        audio_clips.append(audio_clip)

        # Create the flowing text video clip, match the audio duration
        video_clip = create_flowing_text_clip(image_paths[i], scene.captions, audio_clip.duration, scene.narration)
        clips.append(video_clip)

    print("\nConcatenating all scenes and exporting (this might take a minute)...")
    final_video = concatenate_videoclips(clips)
    final_audio = concatenate_audioclips(audio_clips)
    final_video = final_video.with_audio(final_audio)

    output_file = os.path.join(output_dir, "final_short.mp4")
    final_video.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac", logger=None)

    return output_file