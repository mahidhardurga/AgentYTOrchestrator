import os
import time
import base64
from google import genai
from agents.script_agent import ShortScript

def generate_visuals(script: ShortScript, output_dir: str = "output_assets") -> list[str]:
    """
    Generates one image per scene using Gemini 3 Pro Image.
    Returns a list of file paths to the generated image files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    client = genai.Client(api_key=os.environ["OPENAI_API_KEY"])

    print(f"\n--- GENERATING VISUALS FOR {len(script.scenes)} SCENES ---")
    image_files = []

    for scene in script.scenes:
        file_name = f"scene_{scene.scene_number}_visual.jpg"
        file_path = os.path.join(output_dir, file_name)

        print(f"Generating image for Scene {scene.scene_number}...")

        prompt = (
            f"{scene.visual_prompt}, visually appealing, highly detailed, "
            f"vibrant colors, clear focus, high quality, masterpiece, "
            f"vertical composition, cinematic lighting, 9:16 aspect ratio"
        )

        max_retries = 3
        for attempt in range(max_retries):
            try:
                interaction = client.interactions.create(
                    model="gemini-2.5-flash-image",
                    input=prompt,
                    response_format={
                        "type": "image",
                        "mime_type": "image/jpeg",
                        "aspect_ratio": "9:16",
                        "image_size": "2K",
                    },
                )

                if not getattr(interaction, "output_image", None):
                    raise RuntimeError("Gemini returned no image output.")

                image_bytes = base64.b64decode(interaction.output_image.data)

                with open(file_path, "wb") as f:
                    f.write(image_bytes)

                image_files.append(file_path)
                break

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  Error: {e}. Retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                else:
                    raise RuntimeError(f"Critical failure generating image for scene {scene.scene_number} after {max_retries} attempts. Error: {e}")

    print("Visuals generation complete!")
    return image_files