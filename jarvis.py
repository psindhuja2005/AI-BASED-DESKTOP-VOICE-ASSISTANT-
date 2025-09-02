import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()

def time() -> None:
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)

def date() -> None:
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")

def wishme() -> None:
    speak("Welcome back, sir!")
    print("Welcome back, sir!")
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
    else:
        speak("Good night, see you tomorrow.")
    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service. Please tell me how may I assist you.")

def screenshot() -> None:
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(img_path)
    speak(f"Screenshot saved as {img_path}.")
    print(f"Screenshot saved as {img_path}.")

def takecommand() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return None
    except Exception as e:
        speak(f"An error occurred: {e}")
        return None

def play_music(song_name=None) -> None:
    song_dir = os.path.expanduser("~\\Music")
    songs = os.listdir(song_dir)
    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]
    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(song_dir, song))
        speak(f"Playing {song}.")
    else:
        speak("No song found.")

def set_name() -> None:
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as file:
            file.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")

def load_name() -> str:
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"

def search_wikipedia(query):
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")

def create_file(name):
    try:
        path = os.path.join(os.path.expanduser("~/Desktop"), f"{name}.txt")
        with open(path, "w") as file:
            file.write("This is a new file created by your assistant.")
        speak(f"File {name}.txt created on Desktop.")
    except Exception as e:
        speak(f"Failed to create file: {e}")

def open_file(name):
    try:
        path = os.path.join(os.path.expanduser("~/Desktop"), f"{name}.txt")
        os.startfile(path)
        speak(f"Opening file {name}.txt.")
    except Exception as e:
        speak(f"Could not open the file: {e}")

def create_folder(name):
    path = os.path.join(os.path.expanduser("~/Desktop"), name)
    try:
        os.makedirs(path)
        speak(f"Folder {name} created on Desktop.")
    except Exception as e:
        speak(f"Could not create folder: {e}")

def open_folder(name):
    path = os.path.join(os.path.expanduser("~/Desktop"), name)
    try:
        os.startfile(path)
        speak(f"Opening folder {name}.")
    except Exception as e:
        speak(f"Could not open the folder: {e}")

if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if "time" in query:
            time()
        elif "date" in query:
            date()
        elif "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            search_wikipedia(query)
        elif "play music" in query:
            song_name = query.replace("play music", "").strip()
            play_music(song_name)
        elif "open youtube" in query:
            wb.open("https://youtube.com")
        elif "open google" in query:
            wb.open("https://google.com")
        elif "open gmail" in query:
            wb.open("https://mail.google.com")
        elif "change your name" in query:
            set_name()
        elif "screenshot" in query:
            screenshot()
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
        elif "shutdown" in query:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break
        elif "restart" in query:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break
        elif "offline" in query or "exit" in query:
            speak("Going offline. Have a good day!")
            break
        elif "create new file" in query:
            name = query.replace("create new file", "").strip()
            create_file(name)
        elif "open file" in query:
            name = query.replace("open file", "").strip()
            open_file(name)
        elif "create new folder" in query:
            name = query.replace("create new folder", "").strip()
            create_folder(name)
        elif "open folder" in query:
            name = query.replace("open folder", "").strip()
            open_folder(name)
