import os

def create_project_structure():
    base_dir = "AgentYTOrchestrator"

    # Define the folder structure
    folders = [
        "",
        "agents",
        "utils"
    ]

    # Define the files to create
    files = {
        ".env": "OPENAI_API_KEY=your_api_key_here\nOPENAI_API_BASE=https://openrouter.ai/api/v1\n",
        "requirements.txt": "langchain\nlangchain-openai\npydantic\npython-dotenv\n",
        "main.py": "# We will put the main orchestration code here\n",
        "agents/__init__.py": "",
        "agents/script_agent.py": "# We will put the LangChain script generator here\n",
        "agents/audio_agent.py": "",
        "agents/visual_agent.py": "",
        "agents/review_agent.py": "",
        "utils/__init__.py": "",
        "utils/video_editor.py": "",
        "utils/youtube_uploader.py": ""
    }

    print(f"Creating project structure in: {os.path.abspath(base_dir)}")

    # Create directories
    for folder in folders:
        dir_path = os.path.join(base_dir, folder)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created folder: {dir_path}")

    # Create files
    for file_path, content in files.items():
        full_path = os.path.join(base_dir, file_path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created file: {full_path}")

    print("\nSuccess! Your project folder is ready. You can now open it in your code editor.")

if __name__ == "__main__":
    create_project_structure()
