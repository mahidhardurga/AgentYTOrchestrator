import os
import shutil
from agents.script_agent import generate_script
from agents.audio_agent import generate_audio
from agents.visual_agent import generate_visuals
from utils.video_editor import edit_video

def clear_output_directory(directory: str = "output_assets"):
    if os.path.exists(directory):
        print(f"\nClearing old files in '{directory}'...")
        shutil.rmtree(directory)
    os.makedirs(directory)

def main():
    print("Welcome to AgentYTOrchestrator!")
    
    # Step 1: Choose or ask for a topic
    topic = input("Enter a topic for your YouTube Short (or press Enter to use a default): ")
    if not topic.strip():
        topic = "Top 3 fascinating facts about deep space exploration"
        print(f"Using default topic: {topic}")
    
    # Step 2: Generate the content/script
    try:
        # Clear previous assets before generating new ones
        clear_output_directory()
        
        script = generate_script(topic)
        
        print("\n--- SCRIPT GENERATED SUCCESSFULLY ---")
        print(f"Title: {script.title}")
        print(f"Description: {script.description}\n")
        
        for scene in script.scenes:
            print(f"Scene {scene.scene_number}:")
            print(f"  Visual Prompt: {scene.visual_prompt}")
            print(f"  Narration: {scene.narration}")
            print(f"  Captions: {scene.captions}\n")
            
        # Step 3: Generate Audio
        audio_paths = generate_audio(script)
        print(f"\nSaved Audio Files to: {audio_paths}")
        
        # Step 4: Generate Visuals (Images)
        image_paths = generate_visuals(script)
        print(f"\nSaved Image Files to: {image_paths}")
        
        # Step 5: The assets are ready to be stitched together
        final_video_path = edit_video(script, image_paths, audio_paths)
        print(f"\nSUCCESS! Your final YouTube Short is ready at: {final_video_path}")

    except Exception as e:
        print(f"An error occurred while generating the script: {e}")

if __name__ == "__main__":
    main()
