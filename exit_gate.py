import os
import cv2
import face_recognition
import numpy as np
import mysql.connector as sqlconnect
from datetime import date
import pyttsx3
from datetime import datetime
from openpyxl import load_workbook



today = date.today()
today = today.strftime('%d:%m:%Y')
c_time = datetime.now().strftime("%H-%M-%S")
print('current', c_time)
today_split  = today.split(':')
day , month , year = today_split

print(day , month , year)

wb = load_workbook("D:\\AI Organization\\entrance\\Excel sheets per day\\"+day+"-"+month+"-"+year+".xlsx")





entrance = "D:\\AI Organization\\entrance\\"+day+"-"+month+"-"+year




def today_interv():
    knownencoding = []

    encodeList =[]
    mylist = os.listdir(entrance)

    print(mylist)

    
    for cu_img in mylist:
        current_img = cv2.imread(f'{entrance}/{cu_img}')
        images.append(current_img)                                                                           
        personName.append(os.path.splitext(cu_img)[0])
    print(personName)

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


speak("System is fully on now")



# Create the videocapture object
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 330)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 220)


while True:
    images = []
    personName = []
    knownencoding = today_interv()
    ret, frame = cap.read()
    faces = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame, 1)
    
    facesCUrrentFrame = face_recognition.face_locations(frame)
    encodeCurrentFrame = face_recognition.face_encodings(frame, facesCUrrentFrame )
    print("facesCUrrentFrame", facesCUrrentFrame)
    cv2.imshow(' Normal ' ,frame)
    if facesCUrrentFrame != [()]:
        for encodeFace, faceLoc in zip(encodeCurrentFrame, facesCUrrentFrame):
            matches = face_recognition.compare_faces(knownencoding, encodeFace )
            FaceDis = face_recognition.face_distance(knownencoding, encodeFace )
            matchindex = np.argmin(FaceDis)
            name = "Unknown"
            
            y1, x2, y2, x1 = faceLoc
            cv2.rectangle(frame, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 9), thickness=2)
            if matches[matchindex]:
                c_time = datetime.now().strftime("%H-%M-%S")
                name = personName[matchindex].upper()
                print(name)
                sh = wb["Sheet1"]
                for i in range(1, 1048576, 1):
                    item = sh[f"C{i}"].value
                    if item == name:
                        print(f"C{i}")
                        sh[f"D{i}"] = c_time
                        break
                wb.save("D:\\AI Organization\\entrance\\Excel sheets per day\\"+day+"-"+month+"-"+year+".xlsx")
                print("matches[matchindex]", matches[matchindex])
            cv2.imshow(' Normal ' ,frame)
            if cv2.waitKey(1)== 13:
                

                cap.release()
                cv2.destroyAllWindows()
                break


