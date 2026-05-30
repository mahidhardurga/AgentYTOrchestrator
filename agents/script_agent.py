# agents/script_agent.py
import os
from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the expected structure of our LLM output
class Scene(BaseModel):
    scene_number: int = Field(description="The sequential number of the scene.")
    visual_prompt: str = Field(description="Detailed prompt for an AI image/video generator to create the background visual. Be descriptive about lighting, subject, and style.")
    narration: str = Field(description="The exact text the voiceover will speak during this scene.")
    captions: List[str] = Field(description="The complete narration broken down into a list of short, sequential phrases (2-4 words max each). Every word from the narration must be included across these phrases.")

class ShortScript(BaseModel):
    title: str = Field(description="A catchy title for the YouTube Short.")
    description: str = Field(description="A brief description for the YouTube video including relevant hashtags.")
    scenes: List[Scene] = Field(description="List of scenes that make up the 60-second short.")

def generate_script(topic: str) -> ShortScript:
    """
    Generates a structured YouTube short script based on a given topic.
    """
    # Initialize the LLM (Using Gemini 2.0 Flash Experimental Free via OpenRouter)
    llm = ChatOpenAI(
        model="deepseek/deepseek-v4-flash", 
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1"),
        temperature=0.7
    )
    
    # Enforce the structured output
    structured_llm = llm.with_structured_output(ShortScript)
    
    # Create the prompt template
    system_instruction = """
    You are an expert YouTube Shorts producer. 
    Your goal is to write a highly engaging, fast-paced 60-second video script based on the user's topic.
    The script must be divided into a series of short scenes. 
    Each scene should have a distinct 'visual_prompt' optimized for an AI image generator to create visually appealing, high-quality images that accurately match the scene content. Focus on vibrant colors, clear subjects, and an engaging composition.
    Each scene must also include 'captions', which is the complete narration split into a list of short, sequential phrases (2-4 words max each). Every word spoken in the narration must appear in the captions so they sync perfectly with the voiceover.
    Keep the hook strong and ensure the total narration takes no more than 60 seconds (approx. 130-150 words total).
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("human", "Create a YouTube short script for the following topic: {topic}")
    ])
    
    # Chain the prompt and the structured LLM
    chain = prompt | structured_llm
    
    print(f"Generating script for topic: '{topic}'...")
    response = chain.invoke({"topic": topic})
    
    return response
