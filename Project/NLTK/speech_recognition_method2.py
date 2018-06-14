import speech_recognition as sr
import time
import os
from gtts import gTTS


def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return data

# Maya is the name of my speech_recognition_"ai"
def maya(data):
    print(data)
    if "hello" in data:
        speak("I am fine")
    # Need to write to file when full stop is in data
    if "full stop" in data:
        data += '.'


time.sleep(2)  # initialization
speak("Hi momo, what can I do for you?")
while True:
    data = recordAudio()
    maya(data)
