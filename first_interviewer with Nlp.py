from lib2to3.pgen2 import token
from os import name, path
#from typing import Text
#from PIL import Image , ImageDraw
#import PIL
import os
from urllib import response
import cv2
import face_recognition
import numpy as np
import mysql.connector as sqlconnect
from datetime import date
import pyttsx3
import datetime
import speech_recognition as sr
import textblob as TextBlob
from transformers import pipeline #,AutoTokenizer, AutoModelForQuestionAnswering , 
model_name = "deepset/roberta-base-squad2"
#tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
#model = AutoModelForQuestionAnswering.from_pretrained(model_name)
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)


today = date.today()
today = today.strftime('%d:%m:%Y')
today_split  = today.split(':')
day , month , year = today_split
day  = int(day)
month = int(month)
year = int(year)
print(day , month , year)
conn = sqlconnect.connect(host= 'localhost',user='root',password='',database='receptionist')
D =str(day)
M = str(month)
Y = str(year)
today_date = D+":"+M+":"+Y
mycursor= conn.cursor()

path_interview = "D:\\AI Organization\\interview\\"+D+"-"+M+"-"+Y
try:
    os.makedirs(path_interview, exist_ok=False)
except FileExistsError:
    # directory already exists
    pass


def today_interv():


    encodeList =[]
    mylist = os.listdir(path_interview)

    print(mylist)

    
    for cu_img in mylist:
        current_img = cv2.imread(f'{path_interview}/{cu_img}')
        images.append(current_img)                                                                           
        personName.append(os.path.splitext(cu_img)[0])
    print(personName)

    #knownencoding = face_encodings(images)
    #def face_encodings(images):
        

    for image in images:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        knownencoding = encodeList
    return knownencoding

    



engine = pyttsx3.init('sapi5')
voices  = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()



def wishme(name):
     
    hour = int(datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak(f"Good Morning {name}")

    elif hour >= 12 and hour< 18 :
        speak(f"Good afternoon {name}")

    else:

        speak(f"Good Evening {name}")


def sentiment(answer):
    emotion = TextBlob(answer)
    x  = emotion.sentiment.polarity

    return x



def interview(name):
    
    
    speak(f"Hey {name}")

    speak(f"{ name } introduce you self")
    intro = takeCommand().lower()

    """    
    introduc = sentiment(intro)
    print(introduc)

    if(introduc <0):
        marks = marks - 5 """

    speak("Good now tell me")
    speak("what you know about our organizagtion")
    info = takeCommand().lower()
    
    speak(info)

    speak("DID you have any experiance")
    experiance = takeCommand().lower()
    
    speak(experiance)
    if experiance =="yes":
        speak("how much experiance you have.")
        expl = takeCommand().lower()
        exp_point = 1
        speak(expl)
    else:
        exp_point = 0
    speak("Where you see yourself after 5 year")
    futur = takeCommand().lower()
    
    speak(futur)

    speak("why we select you?")
    reson = takeCommand().lower()
    skill = reson
    if skill =="hard working" or skill == "honest" or skill =="innovative": 
        speak(reson+"Good ")
        conf_point = 1
    else:
        conf_point = 0
    

    speak("how much sallary you excepting:")
    exp_salery = takeCommand().lower()
    
    speak("Good")
    
    

    engine.runAndWait()
    
    if exp_point == 1 and conf_point == 0  or exp_point == 0 and conf_point == 1:
        speak("We are offering you Internship ")
        offer = 'internship'
        decision = 'internship'
    elif exp_point == 1 and conf_point == 1:
        speak("We are selected you for second interview Please Be their at 4PM today")
        offer = '2nd interview'
        decision = '2nd interview'
    elif exp_point == 0 and conf_point == 0:
        speak("currently we are short listing the canidate IF you are short listed you will get a call")
        offer = 'reject'
        decision = 'reject'
    else:
        print("we tell you shortly")
    reson = 'Null'
    #decision = 'reject'
    print("uuuuu", exp_point ,conf_point)

    insert_counter = "INSERT INTO counter VALUES(%s,%s, %s, %s)"
    vlu = ("NULL", today_date, ticket , decision )

    mycursor.execute(insert_counter, vlu)
    conn.commit()

    print("Query", name , today_date , experiance , offer ,'responce' ,exp_salery ,'N/A' , decision)
    interview_query = "INSERT INTO interview_results VALUES (%s,%s,%s ,%s ,%s ,%s ,%s ,%s , %s, %s)  "
    values = ("NULL",cnic, name , today_date , experiance , offer , skill ,exp_salery ,'N/A' , decision )

    mycursor.execute(interview_query, values)
    conn.commit()

    

def takeCommand():
    
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("listing")
        r.pause_threshold = 0.5
        r.energy_threshold = 209
        audio =  r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio,  language='en-in')
        print(f"user said: {query}\n ")

    except Exception as e:
        print(e)

        print("Say that again Please.....")
        return "None"

    return query




# Create the videocapture object
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 430)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)


while True:
    images = []
    personName = []
    knownencoding = today_interv()
    ret, frame = cap.read()
    #faces = cv2.resize(frame, (0,0), None, 0.25, 0.25)
    faces = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame, 1)
    
    facesCUrrentFrame = face_recognition.face_locations(frame)
    encodeCurrentFrame = face_recognition.face_encodings(frame, facesCUrrentFrame )
    #cv2.imshow(' Normal ' ,frame)
    for encodeFace, faceLoc in zip(encodeCurrentFrame, facesCUrrentFrame):
        matches = face_recognition.compare_faces(knownencoding, encodeFace )
        FaceDis = face_recognition.face_distance(knownencoding, encodeFace )

        matchindex = np.argmin(FaceDis)
        name = "Unknown"
        y1, x2, y2, x1 = faceLoc
        #y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(frame, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 9), thickness=2)
        if matches[matchindex]:
            ticket = personName[matchindex].upper()
            print(ticket)


            query = (f'select name,ticket, cnic from interview where ticket = {ticket} and date_visit = "{today_date}"'  ) 
               
            result = mycursor.execute(query)
            select = mycursor.fetchall()
            print(select)
            if len(select) >= 1:
                name = list(select)[0][0]
                ticket = list(select)[0][1]
                cnic = list(select)[0][2]
                ticket = int(ticket)
                print("ye wali:", type(today_date))
                counter_Query = (f"select * from counter WHERE  date = '{today_date}'")
                result = mycursor.execute(counter_Query)
                select = mycursor.fetchall()
                counter = len(select) +1
                print("select", name, ticket)
                if ticket > counter :
                    speak(f"please wait we are now serving ticket number {counter}")
                elif ticket == counter:
                    
                    interview(name)

                elif ticket < counter:
                    speak("you lost your turn you can go home now.")
            else:
                speak("register your self first")

        if cv2.waitKey(1)== 13:
            

            cap.release()
            cv2.destroyAllWindows()
            break




