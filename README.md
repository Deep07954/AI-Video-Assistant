# AI Video Assistant

AI Video Assistant is a smart meeting intelligence project that turns audio/video content into structured insights. It can ingest a YouTube link or local media file, transcribe the conversation, summarize it, extract decisions and action items, and let you ask questions about the content using a retrieval-augmented generation (RAG) pipeline.

This project is built for meeting recordings, webinars, interviews, and other spoken content where you need quick understanding and searchable context.
LIVE DEMO- https://ai-video-assistant-caxqcrjya7jx8x7trdnrpu.streamlit.app/

## Features

- YouTube / local media ingestion
  - Downloads audio from YouTube URLs using `yt-dlp`
  - Converts local video/audio files into WAV format
  - Splits large audio into manageable chunks for processing

- Automatic transcription
  - Uses local OpenAI Whisper for English transcripts
  - Supports Hinglish transcription via the Sarvam AI STT API
  - Handles long audio by chunking and combining transcript segments

- AI-powered meeting summarization
  - Generates a professional meeting title
  - Summarizes long transcripts into concise bullet-point output
  - Uses OpenRouter-backed LLM orchestration through LangChain

- Structured extraction
  - Extracts action items with owner and deadline when available
  - Extracts key decisions from the discussion
  - Extracts unresolved questions or follow-up topics

- Meeting Q&A via RAG
  - Creates a vector store with Chroma
  - Uses sentence-transformers embeddings to index transcript chunks
  - Answers questions based only on transcript context
  - Supports conversational follow-up questions after analysis

- Streamlit web app
  - Modern dark-themed interface
  - Sidebar for YouTube URL / file path input
  - Language selector (`english` or `hinglish`)
  - Real-time pipeline status indicators
  - Chat panel for asking questions about the analyzed meeting

- PDF/TXT compatibility in UI flow
  - The app can also accept `.pdf` and `.txt` input files directly for transcript-based analysis

## Tech Stack

- Python
- Streamlit
- LangChain
- OpenRouter / OpenAI-compatible LLM APIs
- Whisper
- Sarvam AI STT API
- ChromaDB
- Hugging Face sentence-transformers
- yt-dlp / pydub / ffmpeg
- NumPy, tqdm, python-dotenv

## Project Structure

```text
AI-Video-Assistant--main/
├── app.py                     # Streamlit UI application
├── main.py                   # CLI pipeline runner
├── Requirements.txt          # Python dependencies
├── test.py                   # Example script for transcript generation
├── .env                      # Local environment variables (not committed)
├── core/
│   ├── extractor.py          # Action item / decision / question extraction
│   ├── rag_engine.py         # RAG prompt + question answering pipeline
│   ├── summarizer.py         # Meeting summary and title generation
│   ├── transcriber.py        # Whisper / Sarvam transcription logic
│   └── vector_store.py       # Chroma vector store setup and retrieval
├── utils/
│   └── audio_processor.py    # Download, convert, and chunk audio
├── downloades/               # Downloaded audio files
├── vector_db/                # Chroma persistent storage
└── venv/                     # Local virtual environment
```

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r Requirements.txt
```

If the environment is missing system FFmpeg on your machine, install it separately because the project uses it for audio conversion and extraction.

## Environment Variables

Create a `.env` file in the project root with the required keys:

```env
OPENROUTER_API_KEY=your_openrouter_key

# Optional: only needed if you use the Hinglish/Sarvam transcription mode
SARVAM_API_KEY=your_sarvam_key
WHISPER_MODEL=small
SARVAM_STT_MODEL=saaras:v2.5
```

Notes:
- `OPENROUTER_API_KEY` is required for the LLM summarization and extraction pipeline.
- `SARVAM_API_KEY` is required only if you choose the `hinglish` language mode.
- `WHISPER_MODEL` defaults to `small` if not set.

## How It Works

The pipeline follows this flow:

1. Input is accepted as a YouTube URL, local audio/video file, or PDF/TXT transcript file.
2. For audio/video input:
   - the file is downloaded or converted to WAV
   - the audio is split into chunks
3. Transcription is performed:
   - English: Whisper
   - Hinglish: Sarvam AI STT translation pipeline
4. Transcript is analyzed through LangChain LLM chains to generate:
   - title
   - summary
   - action items
   - key decisions
   - open questions
5. Transcript chunks are stored in Chroma vector DB.
6. A RAG chain answers user queries grounded in transcript content.
7. Results are displayed in the Streamlit interface.

## Running the App

Run the Streamlit frontend:

```bash
streamlit run app.py
```

Then:
- paste a YouTube URL or file path in the sidebar
- select the language (`english` or `hinglish`)
- click the Analyse button
- review the AI-generated summary, decisions, questions, and transcript
- ask follow-up questions in the chat box

## Running the CLI Version

The project also includes a command-line entry point:

```bash
python main.py
```

You will be prompted to enter:
- a YouTube URL or local file path
- the language (`english` or `hinglish`)

After processing, it prints the generated title, summary, action items, decisions, and supports a chat loop for transcript questions.

## Example Usage

### English transcription

```python
from main import run_pipeline

result = run_pipeline("https://www.youtube.com/watch?v=example", language="english")
print(result["title"])
print(result["summary"])
```

### Hinglish transcription

```python
result = run_pipeline("/path/to/meeting.mp4", language="hinglish")
```

## Notes and Limitations

- The project depends on external AI services and may require valid API keys.
- Large audio files can take time to process depending on model size and hardware.
- Transcription quality depends on audio clarity, speaker overlap, and the chosen language model.
- The app uses local Chroma storage in the `vector_db` folder and persists vectors across runs.
- The project is optimized for meeting-style content and transcript-based Q&A rather than general-purpose video editing or analytics.

## License

This project does not currently include a custom license file. Please check the repository state and add a license if you plan to distribute or publish the project externally.

## Future Enhancements

Potential improvements include:
- speaker diarization
- multi-language support beyond English/Hinglish
- PDF export of summaries and action items
- meeting analytics dashboard
- improved chunking and caching for faster repeated runs
- user authentication and saved meeting history
