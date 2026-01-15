import streamlit as st
from crewai import Crew, Process
from crewai_tools import YoutubeVideoSearchTool
from agents import create_agents
from tasks import create_tasks


st.set_page_config(
    page_title="YouTube Videos to Blog Generator",
    layout="centered"
)

try:

    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

except KeyError:

    st.error("OPENAI_API_KEY not found. Please add it to secrets.toml.")
    st.stop()

st.title("YouTube to Blog Generator")
st.caption(
    "Generate structured, long-form blog posts from YouTube videos using AI agents."
)
st.divider()
st.subheader("Input")

yt_tool = None
topic = None

with st.container(border=True):

    video_url = st.text_input(
        "YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )

    topic = st.text_input(
        "Blog Topic / Title",
        placeholder="Describe what the video is about"
    )

    if video_url and topic:
        yt_tool = YoutubeVideoSearchTool(
            youtube_video_url=video_url
        )

with st.sidebar:

    st.header("Advanced Settings")

    use_cache = st.toggle(
        "Enable Cache",
        value=True,
        help="Reuse previous results to improve performance"
    )

    use_memory = st.toggle(
        "Enable Memory",
        value=True,
        help="Allow agents to retain contextual information"
    )

can_generate = bool(topic and yt_tool)
st.divider()

if not can_generate:
    st.info("Provide a valid YouTube video URL and topic to generate a blog post.")

generate_button = st.button(
    "Generate Blog Post",
    disabled=not can_generate,
    use_container_width=True
)

if generate_button and yt_tool:
    with st.status("Running AI agents...", expanded=True) as status:
        try:
            
            blog_researcher, blog_writer = create_agents(OPENAI_API_KEY)
            blog_researcher.tools = [yt_tool]
            blog_writer.tools = [yt_tool]

            research_task, write_task = create_tasks(
                blog_researcher,
                blog_writer
            )

            research_task.tools = [yt_tool]
            write_task.tools = [yt_tool]

            crew = Crew(
                agents=[blog_researcher, blog_writer],
                tasks=[research_task, write_task],
                process=Process.sequential,
                memory=use_memory,
                cache=use_cache,
                share_crew=True
            )

            result = crew.kickoff(inputs={"topic": topic})

            status.update(
                label="Generation complete",
                state="complete",
                expanded=False
            )

        except Exception as e:
            status.update(
                label="Error occurred",
                state="error",
                expanded=True
            )
            st.error(str(e))
            st.exception(e)
            st.stop()

    st.divider()
    st.subheader("Generated Blog Post")

    try:
        with open("new-blog-post.md", "r", encoding="utf-8") as f:
            blog_content = f.read()
    except FileNotFoundError:
        blog_content = str(result)

    st.markdown(blog_content)
    st.download_button(
        label="Download Markdown",
        data=blog_content,
        file_name=f"{topic.replace(' ', '-').lower()}-blog.md",
        mime="text/markdown"
    )

st.divider()
st.caption("Powered by CrewAI and OpenAI")
