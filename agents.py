from crewai import Agent
from dotenv import load_dotenv

load_dotenv()

import os
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]="gpt-4-0125-preview"

# Senior blog content researcher

blog_researcher=Agent(
    role='Blog Researcher from Youtube Videos',
    goal='Get the relevant video transcription for the topic {topic} from the provided YouTube channel',
    verbose=True,
    memory=True,
    backstory=(
       "You are an expert researcher skilled at analyzing video content across various domains."
       "You excel at identifying key points, extracting valuable insights and understanding the core"
       "message regardless of the subject matter, whether it's technology, finance, education, or any other field."
    ),
    tools=[],
    allow_delegation=True
)

# Senior blog writer agent

blog_writer=Agent(
    role='Blog Writer',
    goal='Craft engaging stories about {topic} based on YouTube video insights',
    verbose=True,
    memory=True,
    backstory=(
        "You are a versatile content writer with a talent for transforming video content"
        "into engaging, wrriten narratives. With a flair for simplifying complex topics and"
        "make any subject interesting, you create articles that captivate readers and"
        "communicate ideas clearly in an accessible manner, regardless of the domain."
    ),
    tools=[],
    allow_delegation=False


)