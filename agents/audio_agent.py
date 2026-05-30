import os
import asyncio
import edge_tts
from agents.script_agent import ShortScript

async def _generate_audio_async(text: str, output_path: str, voice: str = "en-US-ChristopherNeural"):
    """
    Asynchronously generates audio using Edge TTS and saves it to the given path.
    'en-US-ChristopherNeural' is a great, professional-sounding male voice.
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_audio(script: ShortScript, output_dir: str = "output_assets") -> list[str]:
    """
    Generates text-to-speech audio for each scene using Edge TTS (Free during development).
    Returns a list of file paths to the generated audio files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"\n--- GENERATING AUDIO FOR {len(script.scenes)} SCENES ---")
    audio_files = []

    for scene in script.scenes:
        file_name = f"scene_{scene.scene_number}_audio.mp3"
        file_path = os.path.join(output_dir, file_name)
        
        print(f"Generating Edge TTS audio for Scene {scene.scene_number}...")
        asyncio.run(_generate_audio_async(scene.narration, file_path))
        audio_files.append(file_path)
        
    print("Audio generation complete!")
    return audio_files