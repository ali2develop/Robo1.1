import subprocess 
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<Your Key Here>"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client = OpenAI(api_key="<Your Key Here>",
                    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a virtual assistant named robo skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        speak("Opening Linkedin")
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        speak(f"Playing {song}")
        webbrowser.open(link)
    elif "open cap cut" in c.lower():
        try:
            subprocess.Popen([
                "C:\\Users\\GA\\AppData\\Local\\CapCut\\Apps\\CapCut.exe",
                "--src1"
            ])
            speak("Opening CapCut")
        except Exception as e:
            speak("Sorry, I couldn't open CapCut.")
            print(e)
    elif "open free fire" in c.lower():
        try:
            subprocess.Popen([
                "C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe",
                # "--instance", "Nougat32",
                "--cmd", "launchAppWithBsx",
                "--package", "com.dts.freefireth",
                "--source", "desktop_shortcut"
            ])
            speak("Opening Free Fire")
        except Exception as e:
            speak("Sorry, I couldn't open Free Fire.")
            print(e)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])

            # Print the headlines
            for article in articles:
                speak(article['title'])
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
        # Listen for the wake word
    speak("Initializing Robo....")
    while True:"Jarvis"
        
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2)
            word = r.recognize_google(audio)
            if (word.lower() == "robo"):
                speak("Yaa")
                # Listen for command
                with sr.Microphone() as source:
                    audio = r.listen(source)
                    print("Robo Active...")

                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("No Voice {0}".format(e))


