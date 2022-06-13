import os
import cv2
import face_recognition
import numpy as np
import mysql.connector as sqlconnect
from datetime import date
import pyttsx3
import datetime
import speech_recognition as sr
import textblob as TextBlob




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
mark = 0
obyo = 0
path_interview = "D:\\AI Organization\\interview\\"+D+"-"+M+"-"+Y
try:
    os.makedirs(path_interview, exist_ok=False)
except FileExistsError:
    # directory already exists
    pass

print("date", today_date)
def today_interv():
    knownencoding = []
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



def knoledge(knolegde_check):
    mycursor= conn.cursor()
    take_question = f"select * from {knolegde_check}"
    global obyo
    result = mycursor.execute(take_question)
    select = mycursor.fetchall()
    mark = 0

    itr = len(select)
    print(len(select))
    if len(select) >= 1:
        for i in select:
            if obyo < itr:
                
                question = list(select)[obyo][1]
                opection1 = list(select)[obyo][2]
                opection2 = list(select)[obyo][3]
                opection3 = list(select)[obyo][4]
                opection4 = list(select)[obyo][5]
                answer = list(select)[obyo][6]
                print(question, answer)

                print(f"o1:{opection1}\t o2:{opection2}\n o3:{opection3}\t o4:{opection4}")
                user_ans = input("please select opection:")
                
                if(user_ans == answer):
                    mark = mark + 1

                else:
                    mark = mark + 0
            
            obyo = obyo +1


            print("total marks", mark)
    

    if mark == 5:
        
        knowledge = 'Excellent'
        update_query = (f"UPDATE interview_results SET knowledge = '{ knowledge }' WHERE cnic = '{cnic}' and date = '{ today_date}'")
    if mark == 4:
        
        knowledge = 'good'
        update_query = (f"UPDATE interview_results SET knowledge = '{ knowledge }' WHERE cnic = '{cnic}' and date = '{ today_date}'")
    if mark < 4:
        knowledge = 'poor'

        decide = 'reject'

        update_query = (f"UPDATE interview_results SET knowledge = '{knowledge}', decision= '{decide}' WHERE cnic = '{cnic}' and date = '{today_date}'")
    
    print("update", update_query)
    mycursor.execute(update_query)

    conn.commit()

def takeCommand():
    
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("listing")
        r.pause_threshold = 0.5
        r.energy_threshold = 200
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
    print("facesCUrrentFrame", facesCUrrentFrame)
    #cv2.imshow(' Normal ' ,frame)
    if facesCUrrentFrame != [()]:
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
                print("matches[matchindex]", matches[matchindex])

                query = (f'select name,ticket,cnic from interview where ticket = {ticket} and date_visit = "{today_date}"'  ) 
                
                result = mycursor.execute(query)
                select = mycursor.fetchall()
                print("select",select)
                print(select)
                if len(select) >= 1:
                    name = list(select)[0][0]
                    ticket = list(select)[0][1]
                    cnic = list(select)[0][2]
                    
                    person_visit = (f"select result from counter WHERE  date = '{today_date}' and token_number = '{ticket}'")
                    person_status = mycursor.execute(person_visit)
                    result_person = mycursor.fetchall()
                    print("result_person", result_person)
                    if len(result_person) >= 1:
                        result = list(result_person)[0][0]
                        
                        if result =="reject":
                            speak("you are already rejected in 1st interview Please try again after 3 months")

                        elif result =="internship":
                            speak("2nd Interview for interny will begun now please be seated:")
                            knoledge("interny_interview")
                        elif result =="2nd interview":
                            speak("2nd Interview for job will begun now please be seated:")
                            knoledge("job_interview")
                        
                        else:
                            pass


                    else:
                        speak("some thing went wrong")   


                else:
                    speak("register your self first")
        
            if cv2.waitKey(1)== 13:
                

                cap.release()
                cv2.destroyAllWindows()
                break


