import speech_recognition as sr
import sounddevice as sd
import numpy as np

reconhecedor = sr.Recognizer()

print("Pode falar...")

audio = sd.rec(
    int(5 * 44100),
    samplerate=44100,
    channels=1,
    dtype="int16",
    device=1
)

sd.wait()

import wave
with wave.open("audio.wav", "wb") as arquivo:
    arquivo.setnchannels(1)
    arquivo.setsampwidth(2)
    arquivo.setframerate(44100)
    arquivo.writeframes(audio.tobytes())

audio = sr.AudioData(
    audio.tobytes(),
    44100,
    2
)
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

with open("audio.wav", "rb") as arquivo:
    transcricao = client.audio.transcriptions.create(
        file=("audio.wav", arquivo.read()),
        model="whisper-large-v3-turbo",
        language="pt"
    )

print("Você disse:", transcricao.text)


print("Áudio capturado!")