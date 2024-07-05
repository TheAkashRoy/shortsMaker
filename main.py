import os
from utils import *
from dotenv import load_dotenv
import uuid
import requests
import srt_equalizer
import assemblyai as aai
from video import *

from typing import List
from moviepy.editor import *
from termcolor import colored
from dotenv import load_dotenv
from datetime import timedelta
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip

# Load environment variables
load_dotenv("../.env")


clean_dir("./temp/")
clean_dir("./subtitles/")

def tts(text, filename):
    from gtts import gTTS
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

script = ""
# data = request.get_json()
# paragraph_number = int(data.get('paragraphNumber', 1))  # Default to 1 if not provided
# ai_model = data.get('aiModel')  # Get the AI model selected by the user
# n_threads = data.get('threads')  # Amount of threads to use for video generation
# subtitles_position = data.get('subtitlesPosition')  # Position of the subtitles in the video
# text_color = data.get('color') # Color of subtitle text
sentences = script.split(". ")
sentences = list(filter(lambda x: x != "", sentences))
paths = []
from moviepy.config import change_settings

for sentence in sentences:

    current_tts_path = f"./temp/{uuid.uuid4()}.mp3"
    tts(sentence, filename=current_tts_path)
    audio_clip = AudioFileClip(current_tts_path)
    paths.append(audio_clip)
print(paths)

# Combine all TTS files using moviepy
final_audio = concatenate_audioclips(paths)
tts_path = f"./{uuid.uuid4()}.mp3"
final_audio.write_audiofile(tts_path)

try:
    subtitles_path = generate_subtitles(audio_path=tts_path, sentences=sentences, audio_clips=paths)
except Exception as e:
    print(colored(f"[-] Error generating subtitles: {e}", "red"))
    subtitles_path = None

# Concatenate videos
temp_audio = AudioFileClip(tts_path)
combined_video_path = combine_videos(["./videoplayback.mp4"], temp_audio.duration, 60,  2)

try:
    final_video_path = generate_video(combined_video_path, tts_path, subtitles_path,   2, "center", "#FFFF00")
except Exception as e:
    print(colored(f"[-] Error generating final video: {e}", "red"))
    final_video_path = None
