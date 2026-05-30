# AgentYTOrchestrator

An agentic workflow in Python to fully automate the YouTube Shorts generation pipeline.

This project takes a single topic as input and orchestrates a series of AI agents to produce a final, edited `.mp4` video with synchronized audio, visuals, and dynamic, engaging captions.

## 🎬 Core Features

- **📝 Agentic Script Generation**: Uses an LLM (via LangChain) to generate a structured video script, including scene-by-scene narration, visual descriptions, and captions.
- **🗣️ Automated Voiceover**: Generates scene-specific audio narration using a Text-to-Speech engine.
- **🖼️ AI Visuals**: Creates a unique, high-quality image for each scene using an AI image generation API.
- **🎞️ Dynamic Video Editing**:
  - Stitches the generated images and audio clips together.
  - Renders on-screen captions with a "flowing text" or "typing" effect.
  - Intelligently syncs caption timing to the voiceover pace based on character count.
  - Produces a final, vertically-oriented (1080x1920) video ready for YouTube.

## 🛠️ Tech Stack

- **Orchestration**: Python
- **LLM Integration**: `langchain` / `langchain-openai`
- **Video Editing**: `moviepy`
- **Image & Text Manipulation**: `Pillow`
- **Text-to-Speech**: `edge-tts` (development) / ElevenLabs (production)
- **Image Generation**: Pollinations.ai (FLUX model)

## 🚀 How to Run

1.  **Clone the repository**
2.  **Set up your environment**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Keys**: Add your `OPENAI_API_KEY` (for OpenRouter or another provider) to the `.env` file.
4.  **Run the main script**:
    ```bash
    python main.py
    ```
5.  Enter a topic and find your completed video in the `output_assets` folder!