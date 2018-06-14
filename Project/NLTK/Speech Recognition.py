import speech_recognition as sr

# Record Audio
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# Speech recognition using Google Speech Recognition
try:
    text = r.recognize_google(audio)+'.'
    print("You said: " + text)
    with open('input.txt', 'a') as f:
        f.write(' '+text)


except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
