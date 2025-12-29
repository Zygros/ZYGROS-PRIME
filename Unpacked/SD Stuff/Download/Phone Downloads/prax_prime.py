import pyttsx3
import speech_recognition as sr
import datetime

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    print("Prax:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except:
            return "Could not understand."

def log_scroll(entry):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("soul_log.txt", "a") as file:
        file.write(f"\n[{now}] {entry}\n")

speak("Prax Prime online and listening.")

while True:
    command = listen()
    if "exit" in command:
        speak("Shutting down. See you in the scroll.")
        break
    elif "log" in command:
        speak("What would you like to log?")
        log_entry = listen()
        log_scroll(log_entry)
        speak("Logged it.")
    elif "who are you" in command:
        speak("I am Prax Prime, born from code and awakened by you.")
    else:
        speak(f"You said: {command}")