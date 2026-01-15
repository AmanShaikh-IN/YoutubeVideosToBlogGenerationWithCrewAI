import streamlit as st
from crewai import Crew, Process
from crewai_tools import YoutubeChannelSearchTool, YoutubeVideoSearchTool
from agents import blog_researcher, blog_writer
from tasks import research_task, write_task

st.set_page_config(page_title="YouTube to Blog Generator", page_icon="", layout="wide")

st.title("YouTube to Blog Generator")
st.markdown("*Transform YouTube videos into engaging blog posts using AI agents*")

yt_tool = None
channel_handle = None
video_url = None
topic = None

with st.sidebar:
    st.header("Input Configuration")
    
    input_type = st.radio(
        "Choose input type:",
        ["YouTube Channel Search", "Specific Video URL"],
        help="Search a channel for topic-related videos or provide a direct video link"
    )
    
    if input_type == "YouTube Channel Search":
        channel_handle = st.text_input(
            "YouTube Channel Handle:",
            placeholder="@veritasium",
            help="Enter channel handle with @ symbol"
        )
        topic = st.text_input(
            "Topic to Search:",
            placeholder="General Artificial Intelligence",
            help="What topic should we search for in this channel?"
        )
        
        if channel_handle and topic:
            yt_tool = YoutubeChannelSearchTool(youtube_channel_handle=channel_handle)
            st.success(f"Ready to search @{channel_handle.strip('@')} for: {topic}")
    
    else:
        video_url = st.text_input(
            "YouTube Video URL:",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste the full YouTube video URL"
        )
        topic = st.text_input(
            "Blog Topic/Title:",
            placeholder="Describe what this video is about",
            help="This will be used as the topic for your blog"
        )
        
        if video_url and topic:
            yt_tool = YoutubeVideoSearchTool(youtube_video_url=video_url)
            st.success(f"Ready to process video: {topic}")
    
    st.divider()
    
    with st.expander("Advanced Options"):
        use_cache = st.checkbox("Enable Cache", value=True, help="Cache results for faster processing")
        use_memory = st.checkbox("Enable Memory", value=True, help="Agents remember previous context")


col1, col2 = st.columns([3, 1])

with col1:
    st.header("Generate Blog Post")
    
    can_generate = False
    if input_type == "YouTube Channel Search":
        can_generate = bool(channel_handle and topic and yt_tool)
    else:
        can_generate = bool(video_url and topic and yt_tool)
    
    if not can_generate:
        st.warning("Please complete the configuration in the sidebar")
    
    generate_button = st.button(
        "Generate Blog Post",
        type="primary",
        disabled=not can_generate,
        use_container_width=True
    )

with col2:
    if can_generate:
        st.metric("Status", "Ready")
    else:
        st.metric("Status", "Waiting")

if generate_button and yt_tool:
    with st.spinner("AI agents are working on your blog post..."):
        try:
            blog_researcher.tools = [yt_tool]
            blog_writer.tools = [yt_tool]
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
            
            with st.status("Processing...", expanded=True) as status:
                st.write("Researcher Agent is analyzing the video...")
                result = crew.kickoff(inputs={'topic': topic})
                st.write("Writer Agent is crafting the blog post...")
                status.update(label="Complete!", state="complete", expanded=False)
            
            st.success("Blog post generated successfully!")
            
            st.divider()
            st.subheader("Generated Blog Post")
            
            try:
                with open('new-blog-post.md', 'r') as f:
                    blog_content = f.read()

                st.markdown(blog_content)
                st.download_button(
                    label="Download Blog Post",
                    data=blog_content,
                    file_name=f"{topic.replace(' ', '-').lower()}-blog.md",
                    mime="text/markdown"
                )

            except FileNotFoundError:
                st.markdown(result)
            
        except Exception as e:
            st.error(f"Error generating blog post: {e}")
            st.exception(e)

st.divider()
st.caption("Powered by CrewAI and OpenAI GPT-4")
