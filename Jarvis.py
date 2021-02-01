# voice module
import pyttsx3
# Speech recognition module
import speech_recognition as sr

import pywhatkit
import pyjokes
import wikipedia
import datetime
import webbrowser
import smtplib
import subprocess
import json
import requests
import os
import playsound

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    '''
    Accepts speak commands
    :param audio:
    :return:
    '''
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    '''
    Takes voice command through microphone and returns in string format

    :return:
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            #print(e)
            print("I'm Sorry, I didn't catch that")
            return "None"

        return query

def sendEmail(to, content):
    usermail = os.environ.get('EmailUser')
    userpass = os.environ.get('EmailPassword')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(usermail, userpass)
    server.sendmail(usermail, to, content)
    server.quit()

def makeNote(text):
    date = datetime.datetime.now()
    file_name = "myNote.txt"
    with open(file_name, "a") as f:
        date = "[" + str(date) + "] "
        f.write(date)
        f.write(text)
        f.write("\n")

    subprocess.Popen(["notepad.exe", file_name])

def wishMe():
    hour = int(datetime.datetime.now().hour)
    playsound.playsound('Sound/wakeup.mp3', True)
    if hour >=4 and hour <=12:
        speak('Good morning Akhil! How may I help you today')

    elif hour > 12 and hour <=16:
        speak('Good Afternoon Akhil! How may I help you today')

    else:
        speak('Good Evening Akhil! How may I help you today')

    playsound.playsound('Sound/pause.mp3', True)

if __name__ == "__main__":
    note_command = ["make a note", "write it down", "remember this"]
    wishMe()
    while True:
        command = takeCommand().lower()

        if 'jarvis' in command:
            playsound.playsound('Sound/wakeup.mp3', True)

            command = takeCommand().lower()

            for phrase in note_command:
                if phrase in command:
                    speak('What would you like me to write down?')
                    mynote = takeCommand().lower()
                    makeNote(mynote)
                    speak("I've made a note of that")

            if 'wikipedia' in command:
                command = command.replace("search", "searching")
                speak(command)
                query = command.replace("searching","")
                query = query.replace("on wikipedia", "")
                print(query)
                try:
                    result = wikipedia.summary(query, sentences=1)
                    speak('According to Wikipedia')
                    speak(result)
                except Exception as e:
                    speak('Sorry! Unfortunately, there was some issue while searching for result')

            elif 'google' in command:
                searchparam = command.replace("google", "")
                searchquery = 'https://google.com/search?q=' + searchparam
                webbrowser.open(searchquery)

            elif 'youtube' in command:
                searchparam = command.replace("youtube", "")
                searchquery = 'https://www.youtube.com/results?search_query=' + searchparam
                webbrowser.open(searchquery)

            elif 'the time' in command:
                strTime = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The time is {strTime}")

            elif 'send email' in command:
                try:
                    mailList = {}
                    with open('EmailList.txt', 'r') as f:
                        for line in f:
                            line = line.lower().replace('\n', '')
                            (key, val) = line.split(':')
                            key = key.strip()
                            val = val.strip()
                            mailList[key] = val

                    command = command.replace('send email to', '')
                    mailaddr = mailList[command.lower().strip()]

                    while True:
                        speak('What should the email say?')
                        content = takeCommand()
                        speak('confirm message')
                        speak(content)
                        speak('Say yes to confirm and no for new message')
                        answer = takeCommand()
                        if answer.lower() == 'yes':
                            break

                    content = "Subject: 'Automated email from J.A.R.V.I.S' \n\n" + content
                    speak(f'Sending email to {command}')
                    to = mailaddr
                    sendEmail(to, content)
                    speak('Email has been sent')
                except Exception as e:
                    print(e)
                    speak('Sorry Akhil! I am not able to send the email right now')

            elif 'play' in command:
                try:
                    command = command.replace('play', '')
                    if command == "":
                        speak("I'm sorry, I didn't catch that")
                    else:
                        speak(f'Playing {command}')
                        pywhatkit.playonyt(command)
                except Exception as e:
                    speak(f'Sorry! Unable to play {command} right now ')

            elif 'tell me a joke' in command:
                speak(pyjokes.get_joke())

            elif "weather" in command:
                api_key = "8ef61edcf1c576d65d836254e11ea420"
                base_url = "https://api.openweathermap.org/data/2.5/weather?"
                city_name = command.split()[-1]
                complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                response = requests.get(complete_url)
                x = response.json()
                if x["cod"] != "404":
                    y = x["main"]
                    current_temperature = float(y["temp"]) - 273.15
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    speak(" The current temperature is " +
                          str(round(current_temperature)) + "degree celsius"
                          "\n humidity is " +
                          str(current_humidiy) + "percent")
                    print(" Temperature in celsius = " +
                          str(current_temperature) +
                          "\n humidity (in percentage) = " +
                          str(current_humidiy) +
                          "\n description = " +
                          str(weather_description))

                else:
                    speak(" I'm sorry! Seems like there was some issue getting the details for " + city_name)

            elif 'what are you' in command or 'introduce yourself' in command:
                speak("I am Jarvis, your personal assistant.")


            elif 'goodbye' in command or 'bye' in command:
                speak('Goodbye Akhil, turning off')
                playsound.playsound('Sound/turnoff.mp3', True)
                break

            elif 'none' in command:
                speak("I'm sorry, I didn't catch that")

            elif 'thank you' in command:
                speak("You're welcome, Is there anything else I can help you with?")

            else:
                speak("I'm sorry, I'm not programmed for that")

            playsound.playsound('Sound/pause.mp3', True)



