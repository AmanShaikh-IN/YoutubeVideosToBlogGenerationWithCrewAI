from crewai import Agent

def create_agents(api_key: str):
    
    blog_researcher = Agent(
        role="Blog Researcher from Youtube Videos",
        goal="Get the relevant video transcription for the topic {topic} from the provided YouTube channel",
        verbose=True,
        memory=True,
        backstory=(
            "You are an expert researcher skilled at analyzing video content across various domains. "
            "You excel at identifying key points, extracting valuable insights, and understanding the core "
            "message regardless of the subject matter."
        ),
        allow_delegation=True,
        llm="gpt-4o-mini"
    )

    blog_writer = Agent(
        role="Blog Writer",
        goal="Craft engaging stories about {topic} based on YouTube video insights",
        verbose=True,
        memory=True,
        backstory=(
            "You are a versatile content writer with a talent for transforming video content "
            "into engaging written narratives. You simplify complex topics and make any subject "
            "interesting while keeping the content accessible."
        ),
        allow_delegation=False,
        llm="gpt-4o-mini"  
    )

    return blog_researcher, blog_writer