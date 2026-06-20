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
    captions: List[str] = Field(description=
                                """
                                Break the entire narration verbatim into a sequence of short on-screen captions.

                                Requirements:
                                - Every single word from the narration MUST be included in the captions.
                                - Do NOT skip any filler words, connectors, or punctuation.
                                - The captions, when read in sequence, must exactly recreate the full narration.
                                - Each caption should contain 2 to 5 words.
                                - Do NOT overlap words between consecutive captions.
                                - Break the text naturally at pauses, commas, or logical groupings.

                                Example:
                                Narration:
                                "Artificial intelligence started as a simple research project."

                                Captions:
                                [
                                    "Artificial intelligence",
                                    "started as",
                                    "a simple",
                                    "research project."
                                ]
                                """)

class ShortScript(BaseModel):
    title: str = Field(description="A catchy title for the YouTube Short.")
    description: str = Field(description="A brief description for the YouTube video including relevant hashtags.")
    scenes: List[Scene] = Field(description="List of scenes that make up the 60-second short.")

def generate_script(topic: str) -> ShortScript:
    """
    Generates a structured YouTube short script based on a given topic.
    """
    # Initialize the LLM (Using Gemini directly via OpenAI-compatible endpoint)
    model = os.getenv("SCRIPT_MODEL", "gemini-3.5-flash")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing from environment variables")
    llm = ChatOpenAI(
        model=model, 
        api_key=api_key,
        base_url=os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta/openai/"),
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
    Each scene must also include 'captions', which is the complete narration split into sequential chunks of 2-5 words. You must include EVERY word from the narration without skipping filler words, so the captions perfectly reconstruct the voiceover for exact audio synchronization. Do not overlap words between consecutive captions.
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
