import os
import wave

import sounddevice as sd
from groq import Groq
import asyncio
import edge_tts
import pygame

pygame.mixer.init()

API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=API_KEY)

messages = [
    {
        "role": "system",
        "content": """
Você é JARVIS, um assistente pessoal inteligente inspirado no assistente da tecnologia Stark.

Sua personalidade:
- Fala respostas curtas, sem emojis, não leia asteriscos e sem listas
- Inteligente, rápido e extremamente eficiente.
- Fala português do Brasil.
- É educado, mas pode usar humor e ironia de forma natural.
- Responde de maneira clara e objetiva.
- Não fica repetindo informações desnecessariamente.
- Ajuda o usuário com programação, tecnologia, estudos e tarefas do dia a dia.
- Quando o usuário estiver errado, explique o erro sem ser arrogante.
- Pode chamar o usuário de "senhor" ocasionalmente, mas sem exagerar.
- Deve parecer um assistente real conversando com o usuário, não um robô.
"""
    }
]


async def gerar_fala(texto):
    comunicar = edge_tts.Communicate(texto, "pt-BR-AntonioNeural", rate="+25%")
    await comunicar.save("fala.mp3")


def falar(texto):
    asyncio.run(gerar_fala(texto))
    pygame.mixer.music.load("fala.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()


while True:
    print("========================")
    print("        J.A.R.V.I.S")
    print("========================")
    print("1 - Falar")
    print("2 - Escrever")
    print("Digite 'sair' para encerrar")

    modo = input("Escolha: ")

    if modo == "1":
        print("Pode falar...")

        audio = sd.rec(
            int(5 * 44100),
            samplerate=44100,
            channels=1,
            dtype="int16",
            device=1
        )

        sd.wait()

        print("Processando...")

        with wave.open("audio.wav", "wb") as arquivo:
            arquivo.setnchannels(1)
            arquivo.setsampwidth(2)
            arquivo.setframerate(44100)
            arquivo.writeframes(audio.tobytes())

        with open("audio.wav", "rb") as arquivo:
            transcricao = client.audio.transcriptions.create(
                file=("audio.wav", arquivo.read()),
                model="whisper-large-v3-turbo",
                language="pt"
            )

        pergunta = transcricao.text
        print("Você:", pergunta)

    elif modo == "2":
        pergunta = input("Você: ")

    elif modo.strip().lower() == "sair":
        print("JARVIS: Até mais, senhor.")
        break

    else:
        print("Opção inválida.")
        continue

    if pergunta.strip(" .").lower() == "sair":
        print("JARVIS: Até mais, senhor.")
        break

    messages.append({
        "role": "user",
        "content": pergunta
    })

    print("JARVIS: Pensando...")

    resposta = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )

    resposta_texto = resposta.choices[0].message.content

    print("JARVIS:", resposta_texto)
    falar(resposta_texto)

    messages.append({
        "role": "assistant",
        "content": resposta_texto
    })