import os
import requests
from agents.script_agent import ShortScript
from dotenv import load_dotenv

load_dotenv()

def generate_audio(script: ShortScript, output_dir: str = "output_assets") -> list[str]:
    """
    Generates highly realistic text-to-speech audio for each scene using ElevenLabs.
    Returns a list of file paths to the generated audio files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"\n--- GENERATING AUDIO FOR {len(script.scenes)} SCENES ---")
    audio_files = []

    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    if not elevenlabs_api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is missing from .env")

    # Voice ID for "Adam" - a very popular, natural, and energetic voice for Shorts
    voice_id = "pNInz6obpgDQGcFmaJgB" 
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_api_key
    }

    for scene in script.scenes:
        file_name = f"scene_{scene.scene_number}_audio.mp3"
        file_path = os.path.join(output_dir, file_name)
        
        print(f"Generating ElevenLabs audio for Scene {scene.scene_number}...")
        try:
            payload = {
                "text": scene.narration,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                audio_files.append(file_path)
            else:
                raise RuntimeError(f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            raise RuntimeError(f"Critical failure generating audio for scene {scene.scene_number}: {e}")
        
    print("Audio generation complete!")
    return audio_files