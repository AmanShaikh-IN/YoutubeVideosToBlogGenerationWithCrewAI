# Multi Agent CrewAI-Based YouTube Videos to Blog Generator

An **end-to-end, cloud-hosted multi-agent content generation system** that converts YouTube videos into structured, long-form blog posts with the help of external tools.
The application orchestrates specialized AI agents using **CrewAI** to research video content, extract key insights, and transform them into engaging written articles.

Built using **CrewAI**, **OpenAI**, **Streamlit Cloud**, and **YouTube tooling**, it demonstrates agent-based task decomposition and sequential reasoning in a practical content creation pipeline.

---

## Features
- Convert YouTube videos into long-form blog posts
- Multi-agent collaboration (researcher + writer)
- Automatic video transcription analysis
- Structured Markdown blog output
- Downloadable blog posts
- Optional agent memory and caching
- Simple Streamlit-based UI

---

## Demo

### Input
![Input screen](docs/media/Input.png)

### Blog Generation
![Agent execution](docs/media/Generated_Blog_Post.png)

### Output Download
![Generated blog](docs/media/Downloadable_Output.png)

---

## Architecture

```mermaid
flowchart TD
    U["User / Browser"]
    UI["Streamlit UI"]
    YT["YouTube Video URL"]
    TOOL["YouTube Search Tool"]
    
    A1["Blog Researcher Agent"]
    A2["Blog Writer Agent"]
    
    T1["Research Task"]
    T2["Writing Task"]
    
    MD["Markdown Blog Post"]

    U --> UI
    UI --> YT --> TOOL
    TOOL --> A1
    A1 --> T1 --> A2
    A2 --> T2 --> MD
```

## License

MIT License
