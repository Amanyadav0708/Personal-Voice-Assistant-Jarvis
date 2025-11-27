import speech_recognition as sr
import webbrowser
import pyttsx3
import music
import os
import datetime
import subprocess
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

r = sr.Recognizer()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful virtual assistant named Jarvis. Give short, conversational answers suitable for voice output. No special characters.",
                },
                {
                    "role": "user",
                    "content": command,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        response = chat_completion.choices[0].message.content
        print(f"AI Response: {response}")
        speak(response)
    except Exception as e:
        print(f"AI Error: {e}")
        speak("I encountered an error processing your request.")

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://www.whatsapp.com")    
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open  " in c.lower():
        webbrowser.open("https://www.google.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1] 
        link = music.music[song]
        webbrowser.open(link)
    elif "the time" in c.lower():
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"The time is {strTime}")
    elif "the date" in c.lower():
        strDate = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {strDate}")
    elif "open notepad" in c.lower():
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")
    elif "open calculator" in c.lower():
        speak("Opening Calculator")
        subprocess.Popen("calc.exe")
    else:
        # Let AI handle the request
        print(f"Sending to AI: {c}")
        aiProcess(c)
            


if __name__ == "__main__" :
    speak("Initializing Jarvis")
    
    # Calibrate for ambient noise once at startup
    with sr.Microphone() as source:
        print("Calibrating background noise... Please wait.")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Calibration complete.")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for Wake Word...")
                # Short timeout for wake word to keep loop tight
                audio = r.listen(source, timeout=2, phrase_time_limit=3)
            
            word = r.recognize_google(audio)
            
            if "jarvis" in word.lower():
                print("Wake word detected.")
                speak("Yes")
                
                # Listen for the actual command
                with sr.Microphone() as source:
                    print("Jarvis Active - Listening for command...")  
                    # Longer timeout for the actual command
                    audio = r.listen(source, timeout=5, phrase_time_limit=8)
                    
                command = r.recognize_google(audio)
                print(f"Recognized command: {command}")
                processCommand(command)

        except sr.WaitTimeoutError:
            # Normal behavior when no speech is detected within timeout
            pass
        except sr.UnknownValueError:
            # Normal behavior when speech is detected but not recognized
            pass 
        except sr.RequestError as e:
            print(f"Network error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
