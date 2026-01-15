from crewai import Task
from agents import blog_researcher, blog_writer

# Research Task
research_task = Task(
    
  description = (
    "Retrieve and analyze the YouTube video content about {topic}. "
    "Extract the video transcription and identify key points, main arguments, "
    "important examples, and core concepts discussed. "
    "Note timestamps for significant moments if available."
  ),
  expected_output = (
        'A comprehensive research report containing: '
        '1) Video title, channel, and metadata '
        '2) Main topics and subtopics covered '
        '3) Key insights and takeaways (5-7 bullet points) '
        '4) Notable quotes or explanations '
        '5) Supporting examples or case studies mentioned'
  ),
  tools = [],
  agent = blog_researcher,

)

write_task = Task(
  description = (
    "Using the research report, write an engaging blog post about {topic}. "
    "Structure the content with a compelling introduction, well-organized body sections, "
    "and a strong conclusion. Maintain a conversational yet informative tone. "
    "Include relevant examples from the video and ensure the content flows naturally.""
  ),
  expected_output=(
        'A polished blog post (800-1200 words) with: '
        '1) Attention-grabbing title '
        '2) Engaging introduction hook '
        '3) 3-5 main sections with subheadings '
        '4) Concrete examples and explanations '
        '5) Conclusion with key takeaways '
        '6) Formatted in Markdown with proper headings and structure'
    ),
  tools = [],
  agent = blog_writer,
  async_execution = False,
  output_file = 'new-blog-post.md',
  context = [research_task]
)
