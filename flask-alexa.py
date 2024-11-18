from flask import Flask, render_template, redirect, request
import warnings
import threading
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import requests
import os

# Suppress warnings
warnings.filterwarnings('ignore')

# Initialize Flask app
app = Flask(__name__)

# Initialize speech recognition
listener = sr.Recognizer()

# Initialize pyttsx3 engine
def engine_talk(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

# Function to listen to user commands
def user_commands():
    try:
        with sr.Microphone() as source:
            print("Start Speaking!!")
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"Command: {command}")
            return command
    except Exception as e:
        print(f"Error in recognizing speech: {e}")
        return ""

# Function to get weather
def weather(city):
    api_key = "6a22e4b3b349105fe396359fbfaf931f"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        temp_in_celsius = current_temperature - 273.15
        return str(int(temp_in_celsius))
    else:
        return "Unknown"

# Function to process user commands
def run_alexa():
    command = user_commands()
    if not command:
        engine_talk("I didn't hear you properly")
        return

    if 'play a song' in command:
        song = 'Arijit Singh'
        engine_talk('Playing some music')
        pywhatkit.playonyt(song)
    elif 'play' in command:
        song = command.replace('play', '')
        engine_talk(f'Playing {song}')
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        engine_talk(f'Current time is {time}')
    elif 'joke' in command:
        get_j = pyjokes.get_joke()
        engine_talk(get_j)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        engine_talk(info)
    elif 'weather' in command:
        city = 'Hong Kong'
        temp = weather(city)
        engine_talk(f'The temperature in {city} is {temp} degree Celsius')
    elif 'stop' in command:
        engine_talk("Goodbye!")
    else:
        engine_talk("I didn't understand the command.")

# Flask routes
@app.route('/')
def hello():
    return render_template("alexa.html")

@app.route('/home')
def home():
    return redirect('/')

@app.route('/', methods=['POST'])
def submit():
    thread = threading.Thread(target=run_alexa)
    thread.start()
    return render_template("alexa.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
