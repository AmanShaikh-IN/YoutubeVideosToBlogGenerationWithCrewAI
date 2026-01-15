from crewai import Task


def create_tasks(blog_researcher, blog_writer):
    research_task = Task(
        description=(
            "Retrieve and analyze the YouTube video content about {topic}. "
            "Extract the video transcription and identify key points, main arguments, "
            "important examples, and core concepts discussed."
        ),
        expected_output=(
            "A comprehensive research report containing:\n"
            "1) Video title, channel, and metadata\n"
            "2) Main topics and subtopics covered\n"
            "3) Key insights and takeaways (5–7 bullet points)\n"
            "4) Notable quotes or explanations\n"
            "5) Supporting examples or case studies"
        ),
        agent=blog_researcher,
    )

    write_task = Task(
        description=(
            "Using the research report, write an engaging blog post about {topic}. "
            "Structure it with a strong introduction, clear sections, and a conclusion. "
            "Maintain a conversational yet informative tone."
        ),
        expected_output=(
            "A polished blog post (800–1200 words), formatted in Markdown, with:\n"
            "• A compelling title\n"
            "• Clear section headings\n"
            "• Concrete examples\n"
            "• A strong conclusion"
        ),
        agent=blog_writer,
        context=[research_task],
        output_file="new-blog-post.md",
    )

    return research_task, write_task
