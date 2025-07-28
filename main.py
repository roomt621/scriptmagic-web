import gradio as gr
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw
import textwrap
import os, uuid

def generate_image_from_text(text, filename):
    img = Image.new('RGB', (720,480), color=(73,109,137))
    draw = ImageDraw.Draw(img)
    wrapped = textwrap.fill(text, width=40)
    draw.text((40,200), wrapped, fill=(255,255,255))
    img.save(filename)
    return filename

def script_to_video(script, language):
    uid = str(uuid.uuid4())
    img_path = f"{uid}.jpg"
    audio = f"{uid}.mp3"
    video = f"{uid}.mp4"

    generate_image_from_text(script, img_path)
    tts = gTTS(text=script, lang=language)
    tts.save(audio)

    clip = ImageClip(img_path).set_duration(AudioFileClip(audio).duration)
    clip = clip.set_audio(AudioFileClip(audio))
    clip.write_videofile(video, fps=24, codec="libx264", audio_codec="aac")
    os.remove(img_path)
    os.remove(audio)

    return video

interface = gr.Interface(
    fn=script_to_video,
    inputs=[
        gr.Textbox(label="Script"),
        gr.Dropdown(choices=["en", "es", "ur", "hi"], label="Language")
    ],
    outputs="video",
    title="Script to Video Generator",
    description="Generates a video with voiceover from a short script."
)

interface.launch()
