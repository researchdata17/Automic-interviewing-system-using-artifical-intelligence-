
#::: Import modules and packages :::

# Import Keras dependencies
#from importlib.resources import path
from keras.models import model_from_json
#from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
import face_recognition
import cv2
import tensorflow as tf
import mysql.connector as sqlconnect
from datetime import date
import pyttsx3
import datetime
import speech_recognition as sr
import os
from datetime import datetime
import threading
from transformers import pipeline
import logging


model_name = "deepset/roberta-base-squad2"
#tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
#model = AutoModelForQuestionAnswering.from_pretrained(model_name)
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def contex(question, my_text_stream):
    



    question_set = {
        'question': question,
        'context': my_text_stream
    }


    ans = nlp(question_set)
    return ans




today = date.today()
today = today.strftime('%d:%m:%Y')
today_split  = today.split(':')
day , month , year = today_split
day  = int(day)
month = int(month)
year = int(year)
d1 = date(year, month, day)
print(day , month , year)

conn = sqlconnect.connect(host= 'localhost',user='root',password='',database='receptionist')
D =str(day)
M = str(month)
Y = str(year)
mycursor= conn.cursor()
path_interview = "D:\\AI Organization\\interview\\"+D+"-"+M+"-"+Y
try:
    os.makedirs(path_interview, exist_ok=False)
except FileExistsError:
    # directory already exists
    pass

voice_cmd = ""
sond = "on"

engine = pyttsx3.init('sapi5')
voices  = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme(gender):
     
    hour = int(datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak(f"Good Morning {gender}")

    elif hour >= 12 and hour< 18 :
        speak(f"Good afternoon {gender}")

    else:

        speak(f"Good Evening {gender}")        




def takeCommand():
    
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("listing")
        r.pause_threshold = 0.5
        r.energy_threshold = 260  
        #r.dynamic_energy_threshold = True 
        audio =  r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio,  language='en-us')
        print(f"user said: {query}\n ")

    except Exception as e:
        print(e)

        print("Say that again Please.....")
        return "None"

    return query


def OpenListeningModule():  
    logging.info("Opening Microphone")
    #time.sleep(15)
    #speak("microphone started")
    global voice_cmd
    global sond
    speak("microphone started")
    #print("starting loop value = ",sond)
    while True:
        #print("1st:",sond)
        
        while sond == 'on':
            #print("2st:",sond)
            query = " "
            
            r= sr.Recognizer()
            with sr.Microphone() as source:
                #r.adjust_for_ambient_noise(source, duration=0.5)
                print("listing")
                r.pause_threshold = 0.5
                r.energy_threshold = 200  
                #r.dynamic_energy_threshold = True 
                audio =  r.listen(source)

            try:
                #print("Recognizing....")
                query = r.recognize_google(audio,  language='en-us')
                #print(f"user said: {query}\n ")

            except Exception as e:
                print(e)

                print("Say that again Please.....")
                
            voice_cmd = query.lower()
            print(voice_cmd)
            if voice_cmd == "hi" or voice_cmd == "hello" or voice_cmd == "hey":
                sond = 'off'

                #print("exit to outer loop",sond)
                break
        #print("Outerloop Start")        
            #sond = "on"
        #print(sond)
        #if voice_cmd == "exit":
         #   break
    #return 0




tf.autograph.set_verbosity(10)
# ::: Prepare Keras Model :::
# Model files
MODEL_ARCHITECTURE = "D:\\AI Organization Joko Code\\trained models\\gender\\gender_json.json"
MODEL_WEIGHTS = "D:\\AI Organization Joko Code\\trained models\\gender\\gender.h5"




# Load the model from external files
json_file = open(MODEL_ARCHITECTURE)
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# Get weights into the model
model.load_weights(MODEL_WEIGHTS)

# ::: MODEL FUNCTIONS :::
def model_predict(img_path, model):
    
    img =  cv2.resize(img_path, (244, 244))
    img = img_to_array(img)
    img = img.reshape(1, 244,244, 3)
    img = img / 255.0
	
	
	
    model.compile(loss= 'binary_crossentropy', optimizer='adam', metrics = ['accuracy'])
    print(model)

    prediction = model.predict(img)[0][0]
	
    print("Prediction Class: ", prediction)

    return prediction
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 244)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 244)

today_date = D+":"+M+":"+Y
query = (f"select * from interview WHERE  date_visit = '{today_date}'")

print(query)
result = mycursor.execute(query, today_date)
select = mycursor.fetchall()

tic_number = len(select)+1

print("token start with",tic_number)

#camera Settle
def OpenCamera():

    global tic_number
    global date

    x = threading.Thread(target=OpenListeningModule, daemon=True )
    x.start()



    while True:
        while True:
            global voice_cmd
            global sond
            _, frame = cap.read()
            frame = cv2.flip(frame,1)
            cv2.imshow("image",frame)

            if cv2.waitKey(1)== ord('c') or voice_cmd == "hey" or voice_cmd == "hi" or voice_cmd == "hello":
                sond = 'off'
                break

        
        
        Answer = ""
        lst = str(tic_number)
        ticket = lst

        

        face = face_recognition.face_locations(frame, model='hog')
        print("1 ", face)
        if face != []:
            voice_cmd =""
            flag , image = cap.read()
            
            prediction = model_predict(frame, model)
            print(prediction)
            
            if prediction <= 0.5:
                gender = "female"
                Answer = 'MAM'

            elif prediction > 0.5:
                gender = "male"
                Answer = 'SIR'

            wishme(Answer)

            speak("How my i assist you:")
            greeting  = takeCommand().lower()
            print(greeting)
            if  'interview' in greeting:
                speak("Please write your CNIC Number without Dashes:")
                cnic = input()

                cnic_split = cnic.split()
                cnic ="" 
                for i in cnic_split:
                    cnic= cnic+i
                    print(cnic)
                
                print("cnic" , cnic)
                while len(cnic) != 13:
                    speak("Please write correct CNIC number That is 13 Digit long")
                    cnic = input()
                    cnic_split = cnic.split()
                    cnic =""
                    for i in cnic_split:
                        cnic= cnic+i
                    print(cnic)

                
                query = 'select name, date_visit from interview where cnic = ' +str(cnic)+ ''   

                result = mycursor.execute(query)
                select = mycursor.fetchall()


                print(select)
        
                if  select ==[]:
                    speak("What is your good name?")
                    question = "What is your good name?"
                    user_told = takeCommand().lower()

                    ans = contex(question, user_told)
                    name = ans.get('answer')

                    gender = gender
                    #date   = today

                    speak("Please tell me your qualification: ")
                    question = "Please tell your qualification:"
                    user_told = takeCommand().lower()
                    ans = contex(question, user_told)
                    education = ans.get('answer')

                    speak("which isntitue you were studied: ")
                    question = "Please tell your qualification:"
                    user_told = takeCommand().lower()
                    ans = contex(question, user_told)
                    institute = ans.get('answer')

                    purpose = "Interview"

                    
                    tic_number = int(tic_number)+1
                    speak(f'welcome to AI Organisation JOKO your ticket number is {ticket}:')
                    query = "INSERT INTO interview VALUES (%s,%s ,%s ,%s ,%s ,%s ,%s , %s)  "
                    values = (name, gender ,cnic, today_date , education , institute ,purpose , ticket )

                    mycursor.execute(query, values)
                    conn.commit()
                    file = path_interview+"\\"+ticket+'.jpg'
                    cv2.imwrite(file, frame)
                    
                    sond = 'on'
                elif select != []:
                    for i in select:
                        name = list(i)[0]
                        date_visit = list(i)[1]

                    date_visit  = date_visit.split(':')
                    print("last Visit was:", date_visit)
                    day_visit , month_visit , year_visit = date_visit
                    day_visit  = int(day_visit)
                    month_visit = int(month_visit)
                    year_visit = int(year_visit)
                
                    d0 = date(year_visit, month_visit, day_visit)
                    delta = d1 - d0
                    print(delta.days)
                    if delta.days <= 90:
                        speak(f"Dear {name} sorry to inform you that you are not illegible for intervie")
                        speak(f"Because you already gave interview {delta.days} Days ago" )
                        speak("Please try again after 90 days")

                    elif delta.days >90:
                        speak("you may now give interview")
                    
                        sql_updat = "UPDATE interview SET date_visit = %s , ticket = %s WHERE cnic = %s"
                        values = (today, ticket ,cnic)
                        mycursor.execute(sql_updat, values)

                        conn.commit()
                        file = path_interview+"\\"+ticket+'.jpg'
                        cv2.imwrite(file, frame)
                        print(sql_updat)
                        tic_number = tic_number + 1

                    sond ='on'

            elif greeting == 'orientation':
                day = datetime.today().strftime('%A').lower()

                if day == 'saturday':
                    speak("GO to confrance room and orientation will be star at 10PM:")

                else:
                    speak("please Reach on Orientation day that is on Saturday")
                
                sond = 'on'
            else:
                speak("sorry sir i an not able to help you with this:")

                sond = 'on'



if __name__ == "__main__":
    OpenCamera()



