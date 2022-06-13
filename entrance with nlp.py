from ast import Pass
import cv2
import face_recognition
import xlsxwriter
from datetime import datetime
import os
from datetime import date
import pyttsx3
import speech_recognition as sr
import threading
import logging
from transformers import pipeline



engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 143)
voices  = engine.getProperty('voices')

print(voices)
engine.setProperty('voice', voices[1].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

speak("Engion is loading")
model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def contex(my_text_stream):
    



    question_set = {
        'question': 'what is your name?',
        'context': my_text_stream
    }


    ans = nlp(question_set)
    return ans




today = date.today()
today = today.strftime('%d:%m:%Y')
today_split  = today.split(':')
day , month , year = today_split
voice_cmd = ""
path_entrance = "D:\\AI Organization\\entrance\\"+ day + "-" + month + "-" + year
try:
    os.makedirs(path_entrance, exist_ok=False)
except FileExistsError:
    pass





speak("Camera is loading")



voice_cmd = ""
sond = "on"
def takename():
    speak("what is your name")
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("listing")
        r.pause_threshold = 0.5
        r.energy_threshold = 110 
        audio =  r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio,  language='en-in')
        print(f"user said: {query}\n ")

    except Exception as e:
        print(e)

        print("Say that again Please.....")
        return "No Name"

    return query


def OpenListeningModule():  
    logging.info("Opening Microphone")
    global voice_cmd
    global sond
    speak("microphone started")
    while True:

        while sond == 'on':
            
            query = " "
            
            r= sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("listing")
                r.pause_threshold = 0.5
                r.energy_threshold = 207  
                #r.dynamic_energy_threshold = True 
                audio =  r.listen(source)

            try:
                #print("Recognizing....")
                query = r.recognize_google(audio,  language='en-us')
                print(f"user said: {query}\n ")

            except Exception as e:
                print(e)

                print("Say that again Please.....")
                
            voice_cmd = query.lower()
            print(voice_cmd)
            if voice_cmd == "hi" or voice_cmd == "hello" or voice_cmd =="exit" or voice_cmd == "hey":
                sond = 'off'

                break

        if voice_cmd == "exit":
            break


        
       



file_name = "D:\\AI Organization\\entrance\\Excel sheets per day\\"+day+"-"+month+"-"+year+".xlsx"
workbook = xlsxwriter.Workbook(file_name)
worksheet = workbook.add_worksheet()
worksheet.set_column('A:E',25)
worksheet.set_default_row(75)
cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
worksheet.write(0,0, "Person Name", cell_format)
worksheet.write(0,1, "IN-Image", cell_format)
worksheet.write(0,2, "In-Time", cell_format)
worksheet.write(0,3, "Out-Time", cell_format)



# Create the videocapture function and object
def OpenCamera():
    logging.info("Opening camera")
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 430)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
    x = threading.Thread(target=OpenListeningModule, daemon=True )
    x.start()
    row = 1
    col =0
    while True:
        global voice_cmd
        global sond
        now = datetime.now()

        current_time = now.strftime("%H-%M-%S")
        voice_cmd = voice_cmd
        success, frame = cap.read()
        # Show the output


        frame = cv2.flip(frame, 1)
        image = face_recognition.face_locations(frame, model='hog')  
        face_point = list((image))

        print(face_point)
        if image != []:
            y1,x2,y2,x1 =   (face_point)[0]
            if y1 != "" and x2 != "" and y2 != "" and x1 != "":
                frame = cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,2), 2)
            cv2.imshow("Frame", frame)
        else:
            cv2.imshow("Frame", frame)
            Pass
    # If 'c' key is pressed then click picture
        if cv2.waitKey(1) == ord('c') or voice_cmd == "hey" or voice_cmd == "hi" or voice_cmd == "hello":
            #speak("What is your name")
            print("microphone start")
            voice_cmd =""
            
            name = takename()
            my_text_stream = name
            ans = contex(my_text_stream)
            print("ans", ans)
            name = ans.get('answer')
            speak(f"{name} you can go now")
            file = path_entrance+'/'+ current_time + '.jpg'

 
            sond = "on"
            cv2.imwrite(file, frame)
        
            worksheet.write(row, col, name)
            worksheet.insert_image(row, col+1, file, {'x_scale':0.282, 'y_scale': 0.280 ,'x_offset': 0, 'y_offset': 0, 'positioning':1} )
            worksheet.write(row, col+2, current_time)
            
            
            row+=1 
            


        if cv2.waitKey(1)  == ord('q') or voice_cmd == "exit":
            break
        logging.info("Frame Pura")
        #print("action say: ",voice_cmd)
    workbook.close()

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    OpenCamera()
