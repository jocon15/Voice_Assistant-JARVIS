import time
import pyttsx3
import speech_recognition as sr


def speak(text, rate=200):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print('Exception ' + str(e))
    return said
