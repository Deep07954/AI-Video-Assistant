import yt_dlp
import os
import subprocess

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # Handle file extensions properly for yt-dlp output
        base, _ = os.path.splitext(filename)
        wav_path = base + ".wav"
        if not os.path.exists(wav_path):
            # Fallback check
            for ext in ['.webm', '.m4a', '.mp3']:
                if os.path.exists(base + ext):
                    # Convert to wav using ffmpeg directly
                    converted_wav = base + ".wav"
                    subprocess.run(["ffmpeg", "-y", "-i", base + ext, "-ar", "16000", "-ac", "1", converted_wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    wav_path = converted_wav
                    break
    return wav_path

def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to 16kHz mono WAV format using ffmpeg directly."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    # Run ffmpeg command directly: -ar 16000 (16kHz), -ac 1 (Mono)
    cmd = ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", output_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    """Split audio into chunks using ffmpeg segment muxer without pydub."""
    chunk_duration_sec = chunk_minutes * 60
    output_pattern = wav_path + "_chunk_%d.wav"
    
    # Use ffmpeg segment tool for fast and clean audio splitting
    cmd = [
        "ffmpeg", "-y", "-i", wav_path,
        "-f", "segment", "-segment_time", str(chunk_duration_sec),
        "-c", "copy", output_pattern
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Collect generated chunk files
    chunks = []
    i = 0
    while True:
        chunk_path = wav_path + f"_chunk_{i}.wav"
        if os.path.exists(chunk_path):
            chunks.append(chunk_path)
            i += 1
        else:
            break
            
    # Fallback if ffmpeg segment didn't output numbered files cleanly
    if not chunks and os.path.exists(wav_path):
        chunks = [wav_path]
        
    return chunks

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks