import pyttsx3
import pyaudio
import speech_recognition as sr
import sys
import webbrowser
import bs4, requests
import random
from bs4 import BeautifulSoup
from requests_html import HTMLSession

session = HTMLSession()
engine = pyttsx3.init()
#Manual Override
manual = False
print("Enable manual override? (Y/N)")
engine.say("Enable manual override?")
engine.runAndWait()
override = input()
if(override.lower() == "y"):
    print("Manual override enabled")
    engine.say("Manual override enabled")
    manual = True
else:
    print("Voice recognition enabled")
    engine.say("Voice recognition enabled")
print("What's on your mind?")
engine.say("What's on your mind?")
engine.runAndWait()
while(True):
    query = ""
    search = ""
    question = ""
    insert = ""
    output = []
    #Input
    r = sr.Recognizer()
    end = False
    skip = False
    if(manual == False):
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
            except:
                skip = True
    else:
        text = input()
    #Categories
            #Terminate, Math, Google, Youtube, Trivia, Store, Joke, Translate
    store = ["make", "acquire", "build", "read", "clear", "delete", "destroy"]
    trivia = ["who", "what", "when", "where", "why", "how","How", "Who", "What", "Where", "When", "Why"]
    youtube = ["YouTube", "play", "Play"]
    google = ["Google", "search"]
    math = ["math", "calculate"]
    terminate = ["exit", "terminate", "end", "stop", "bye", "goodbye", "close"]
    joke = ["joke", "laugh", "smile"]
    translate = ["translate", "language"]

    #Output
        #Terminate
    if(skip == False):
        tokens = text.split(" ")
        for i in range(len(terminate)):
            if(text == terminate[i]):
                end = True
                break

        if(end == False):
            if(skip == False):
                #Sentiment Values
                disgust = 0
                anger = 0
                sadness = 0
                suprise = 0
                fear = 0
                joy = 0
                trust = 0
                anticipation = 0
                sentiment = 0
                #Sentiment Analysis
                    ##Optimize Using Keystones
                    #Enable/Disable
                data = open(r"sentimentdata.txt","r")
                info = data.readlines()
                for e in range(len(tokens)):
                    for w in range(len(info)):
                        term = info[w].split(",")
                        if(term[0] == tokens[e]):
                            if(term[1] == "anger"):
                                anger += 1
                            if(term[1] == "sadness"):
                                sadness += 1
                            if(term[1] == "fear"):
                                fear += 1
                            if(term[1] == "joy"):
                                joy += 1
                            if(term[1] == "trust"):
                                trust += 1
                            if(term[1] == "anticipation"):
                                anticipation += 1
                            if(term[4] == "negative"):
                                sentiment -= 1
                            if(term[4] == "positive"):
                                sentiment += 1
                            break
                print(sentiment)
                print("Joy: " + str(joy))
                print("Anticipation: " + str(anticipation))
                print("Trust: " + str(trust))
                print("Sadness: " + str(sadness))
                print("Fear: " + str(fear))
                print("Anger: " + str(anger))
                #Joke
                reserve = ["Today at the bank, an old lady asked me to help check her balance. So I pushed her over.",
                           "I bought some shoes from a drug dealer. I don't know what he laced them with, but I've been tripping all day.",
                           "My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away.",
                           "I couldn't figure out why the baseball kept getting larger. Then it hit me.",
                           "Why did the old man fall in the well? Because he couldn't see that well.",
                           "Where do you find a cow with no legs? Right where you left it.",
                           "What did one hat say to the other? You stay here. I’ll go on ahead.",
                           "Why did it take so long for the pirates to learn the Alphabet? They got stuck at C.",
                           "I think i would like a job cleaning mirrors, it's just something I could really see myself doing.",
                           "When a deaf person sees someone yawn do they think it’s a scream?"]
                for jk in range(len(joke)):
                    if(joke[jk] in tokens):
                        jok = random.randrange(0,9)
                        text = (reserve[jok])
                #Translate
                        #Refine Dictionary
                if(tokens[0] == translate[0] or tokens[0] == translate[1]):
                    try:
                        text = ""
                        dictionary = ""
                        msg = 1
                        while(msg < len(tokens)):
                            for tra in range(len(dictionary)):
                                word = dictionary[tra].split(" ")
                                if(tokens[msg] == word[0]):
                                    text += word[1]+" "
                                    break;
                                elif(tokens[msg] == word[1]):
                                    text += word[0]+" "
                                    break;
                            msg += 1
                    except:
                        text = "Please use the proper format, translate command, message. (EN-FR)"

                #Math
                for k in range(len(math)):
                    if(tokens[0] == math[k]):
                        if(len(tokens) > 3):
                            if(tokens[2] == "+" or tokens[2] == "add"):
                                text = int(tokens[1]) + int(tokens[3])
                            if(tokens[2] == "-" or tokens[2] == "subtract" or tokens[2] == "minus"):
                                text = int(tokens[1]) - int(tokens[3])
                            if(tokens[2] == "*" or tokens[2] == "multiply"):
                                text = int(tokens[1]) * int(tokens[3])
                            if(tokens[2] == "divide" or tokens[2] == "divided"):
                                text = int(tokens[1]) / int(tokens[3])
                            if(tokens[2] == "exponent"):
                                text = int(tokens[1]) ** int(tokens[3])
                            if(tokens[2] == "remainder" or tokens[2] == "modulus"):
                                text = int(tokens[1]) % int(tokens[3])
                        break
                #Google
                for j in range(len(google)):
                    if(tokens[0] == google[j]):
                        for m in range(len(tokens)):
                            if(m != 0):
                                query += tokens[m] + " "
                        webbrowser.open("https://google.com/search?q=%s" % query)
                        text = "Searching for: " + query
                        break
                #Youtube
                for b in range(len(youtube)):
                    if(tokens[0] == youtube[b]):
                        for n in range(len(tokens)):
                            if(n != 0):
                                search += tokens[n]
                                if(n != len(tokens)-1):
                                    search += "+"
                        results = requests.get("https://www.youtube.com/results?search_query=%s" % search).content
                        soup = BeautifulSoup(results, "html.parser")
                        for a in soup.find_all("a", href=True):
                            case = a['href']
                            if(len(case) > 1):
                                if(case[1] == "w"):
                                    webbrowser.open("https://www.youtube.com%s" % case)
                                    break
                        text = "Searching for: " + search.replace("+", " ")
                        break
                #Trivia
                for p in range(len(trivia)):
                    if(tokens[0] == trivia[p]):
                        for y in range(len(tokens)):
                            question += tokens[y]
                            if(y != len(tokens)-1):
                                question += " "
                        results = session.get("https://google.com/search?q=%s" % question).content
                        soup = BeautifulSoup(results, "html.parser")
                        try:
                            case = soup.find('div',{'class':'Z0LcW'})
                            if(case == None):
                                case = soup.find('span',{'class':'e24Kjd'})
                            text = case.text
                        except:
                            text = "Sorry, Kiwi encountered an issue"
                #Store
                for q in range(len(store)):
                    if(tokens[0] == store[q]):
                        if(tokens[0] == "make" or tokens[0] == "build"):
                            for v in range(len(tokens)):
                                if(v != 0):
                                    insert += tokens[v] + " "
                            file = open(r"notes.txt", "a")
                            file.write(insert)
                            text = "Notes updated successfully"
                        if(tokens[0] == "acquire" or tokens[0] == "read"):
                            file = open(r"notes.txt", "r")
                            try:
                                output = file.readlines()
                                text = output[0]
                            except:
                                text = "No notes found"
                        if(tokens[0] == "destroy" or tokens[0] == "delete" or tokens[0] == "clear"):
                            file = open(r"notes.txt", "w+")
                            file.write("")
                            text = "Notes successfully cleared"
                engine.say(text)
                print(text)
                engine.runAndWait()
        else:
            engine.say("Kiwi successfully terminated")
            print("Kiwi successfully terminated...")
            engine.runAndWait()
            break
