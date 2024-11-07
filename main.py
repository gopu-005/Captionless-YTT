import streamlit as st
from dotenv import load_dotenv # type: ignore
import os
import google.generativeai as genai # type: ignore
from youtube_transcript_api import YouTubeTranscriptApi # type: ignore
from pytube import YouTube # type: ignore
import requests

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = "AIzaSyCIdEZJK6cu1KsmPHLQGgAAV_H3guA24sQ"

# Configure the Google Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Summarization prompt
prompt = """You are a YouTube Video summarizer. You will take the transcript text and summarize the entire video, providing an important summary in points within 250 words. The summary will be displayed here: """

# Extract transcript using the YouTube Transcript API or fall back to Speech-to-Text
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        
        # Attempt to get the transcript
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([entry['text'] for entry in transcript_text])
        
    except Exception as e:
        # If captions aren't available, fallback to speech-to-text
        transcript = convert_audio_to_text(youtube_video_url)
    
    return transcript

# Download the audio and convert it to text using Speech-to-Text API (e.g., Google Speech-to-Text)
def convert_audio_to_text(youtube_video_url):
    try:
        # Download video audio using pytube
        yt = YouTube(youtube_video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(filename="audio.mp4")
        
        # Convert audio to text (replace with your Speech-to-Text API of choice)
        # Example: Using Google Speech-to-Text API (replace this with actual API code)
        transcript_text = "Transcription text here" # Mock-up, replace with actual speech-to-text conversion
        
        return transcript_text
    
    except Exception as e:
        raise Exception("Error in converting audio to text: " + str(e))

# Generate summary using the Gemini model
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit UI
st.title('YouTube Video Summarizer [Captionless Videos]')
youtube_link = st.text_input('Enter YouTube video link:')

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f'http://img.youtube.com/vi/{video_id}/0.jpg', use_container_width=True)


if st.button('Get Detailed Notes'):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.header('Transcript:')
        st.write(summary)
