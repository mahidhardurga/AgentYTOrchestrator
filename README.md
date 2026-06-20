# AgentYTOrchestrator

An agentic workflow in Python to fully automate the YouTube Shorts generation pipeline, featuring automated review notifications and direct YouTube uploads.

This project takes a single topic as input and orchestrates a series of AI agents to produce a final, edited `.mp4` video with synchronized audio, visuals, and dynamic on-screen captions.

---

## 🎬 Core Features

- **📝 Agentic Script Generation**: Uses Google Gemini (via LangChain's OpenAI-compatible endpoint) to generate a structured video script, including scene-by-scene narration, visual descriptions, and exact word-for-word captions.
- **🗣️ Automated Voiceover**: Generates realistic, scene-specific narration using ElevenLabs Text-to-Speech.
- **🖼️ AI Visuals**: Generates unique, high-quality images for each scene using the Gemini Image API (`gemini-2.5-flash-image` via the `google-genai` SDK).
- **🎞️ Dynamic Video Editing**:
  - Stitches generated images and audio clips together using `moviepy`.
  - Renders customizable on-screen captions with a "flowing text/typing" effect using `Pillow`.
  - Intelligently syncs caption timing to the voiceover narration based on word matching and timing distribution.
  - Produces a final, vertically-oriented (1080x1920) video ready for YouTube.
- **📲 WhatsApp Video Review**: Automatically uploads the generated video to a temporary public host and sends a review request with the video link to your phone using the Twilio WhatsApp API.
- **🚀 Automated YouTube Upload**: Uploads the approved video directly to your YouTube channel as a Short using the YouTube Data API v3.

---

## 🛠️ Tech Stack

- **Orchestration**: Python
- **LLM Integration**: `langchain` / `langchain-openai` (configured for Gemini API)
- **Image Generation**: `google-genai` (Gemini Image Generation)
- **Text-to-Speech**: ElevenLabs API
- **Video Editing & Typography**: `moviepy` & `Pillow`
- **Review Notifications**: Twilio SMS/WhatsApp API
- **YouTube API**: `google-api-python-client` & `google-auth-oauthlib`

---

## ⚙️ Configuration & Setup

### 1. Prerequisites & API Keys
To run the orchestrator, you will need keys/credentials from the following services:
- **Google Gemini API Key**: For script generation and image creation.
- **ElevenLabs API Key**: For text-to-speech voice generation.
- **Twilio Account**: A Twilio SID, Auth Token, and WhatsApp Sandbox setup for sending review notifications.
- **Google Cloud Console Credentials**:
  1. Create a Google Cloud project.
  2. Enable the **YouTube Data API v3**.
  3. Configure the **OAuth Consent Screen** (set application type to **Desktop App**).
  4. Add your channel owner email as a test user.
  5. Go to **Credentials**, create an **OAuth client ID** (Desktop Application), download the JSON credentials, and save it in the root of this project as `client_secret.json`.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure `.env`
Create a `.env` file in the root directory (based on the template below) and add your keys:
```env
# Gemini API Key (Required for both Script and Image Generation)
GEMINI_API_KEY=your_gemini_api_key_here
# GEMINI_API_BASE=https://generativelanguage.googleapis.com/v1beta/openai/

# ElevenLabs Settings
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Twilio WhatsApp Review Settings
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
YOUR_WHATSAPP_NUMBER=whatsapp:+your_mobile_number_here

# Configurable Models (Optional - defaults will be used if omitted)
SCRIPT_MODEL=gemini-3.5-flash
VISUAL_MODEL=gemini-2.5-flash-image
AUDIO_MODEL=eleven_multilingual_v2
AUDIO_VOICE_ID=pNInz6obpgDQGcFmaJgB
```

---

## 🚀 Execution Workflow

Run the main pipeline orchestrator:
```bash
python main.py
```

### Flow of Execution:
1. **Topic Input**: Enter a video topic (or use the default space exploration topic).
2. **Script Generation**: Script agent plans scenes, narration, image prompts, and caption timings.
3. **Voiceover Generation**: ElevenLabs creates narration audio files.
4. **Image Generation**: Gemini renders beautiful, high-resolution vertical images.
5. **Video Compilation**: The video editor stitches everything together, aligns audio, and overlays dynamic typing captions.
6. **WhatsApp Review**: The review agent uploads the draft video to a temp server and notifies you via WhatsApp.
7. **YouTube Upload**: If you reply `yes` to the console prompt, the script authenticates via browser OAuth, saves the credential token (`token_channel2.pickle`), and uploads the video directly to YouTube as a Public Short.