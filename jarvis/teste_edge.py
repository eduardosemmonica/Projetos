import asyncio
import edge_tts

async def falar():
    comunicar = edge_tts.Communicate("Olá, senhor. Todos os sistemas estão operacionais.", "pt-BR-AntonioNeural")
    await comunicar.save("fala.mp3")

asyncio.run(falar())