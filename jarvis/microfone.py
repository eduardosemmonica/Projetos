import sounddevice as sd

print("Gravando por 5 segundos...")

audio = sd.rec(
    int(5 * 44100),
    samplerate=44100,
    channels=1
)

sd.wait()

print("Gravação finalizada!")