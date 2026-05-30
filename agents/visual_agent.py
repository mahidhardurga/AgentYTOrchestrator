import os
import requests
import time
import urllib.parse
from agents.script_agent import ShortScript

def generate_visuals(script: ShortScript, output_dir: str = "output_assets") -> list[str]:
    """
    Generates a vertical image for each scene based on its visual prompt.
    Uses Pollinations.ai with the FLUX model for highly accurate, free image generation.
    Returns a list of file paths to the generated image files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"\n--- GENERATING VISUALS FOR {len(script.scenes)} SCENES ---")
    image_files = []
    
    for scene in script.scenes:
        file_name = f"scene_{scene.scene_number}_visual.jpg"
        file_path = os.path.join(output_dir, file_name)
        
        print(f"Generating image for Scene {scene.scene_number}...")
        
        # Enhance the prompt to ensure a visually appealing and accurate style
        enhanced_prompt = f"{scene.visual_prompt}, visually appealing, highly detailed, vibrant colors, clear focus, high quality, masterpiece"
        
        # Encode the prompt and use the FLUX model which has excellent prompt adherence
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        API_URL = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&model=flux&nologo=true"

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(API_URL, timeout=180)
                
                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    image_files.append(file_path)
                    break  # Success, exit the retry loop
                else:
                    print(f"  Failed to generate image for scene {scene.scene_number}: {response.text}")
                    break  # Don't retry on permanent errors like 401 Unauthorized
            except requests.exceptions.RequestException as e:
                print(f"  Network error ({type(e).__name__}). Retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(5)
        else:
            print(f"  Failed to generate image for scene {scene.scene_number} after {max_retries} attempts.")
            
    print("Visuals generation complete!")
    return image_files