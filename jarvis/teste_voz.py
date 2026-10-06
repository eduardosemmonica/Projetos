import pyttsx3

voz = pyttsx3.init()

vozes = voz.getProperty("voices")
for v in vozes:
    print(v.name, "|", v.id)

voz.say("Olá, senhor.")
voz.runAndWait()