import cv2
import face_recognition
import pyttsx3
import os
import numpy as np
import json
import time

file = open("20_years_planning_names.json")
invitees_list = json.load(file)
file.close()

class Video(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.path = "images2"
        self.images = []
        self.attend = []
        self.its = []
        self.mylist = os.listdir(self.path)
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 150)
        for cl in self.mylist:
            self.curImg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(self.curImg)
            self.its.append(os.path.splitext(cl)[0])

        self.encoded_face_train = self.findEncodings(self.images)
    def __del__(self):
        self.cap.release()

    def speak(self, name, seat):
        self.engine.say(f"Welcome {name} to 20 years plan event. Your seat number is {seat}. Thank you!")
        self.engine.runAndWait()

    def findEncodings(self, images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encoded_face = face_recognition.face_encodings(img)[0]
            encodeList.append(encoded_face)
        return encodeList
    def get_frame(self):
        final = []
        success, img = self.cap.read()
        print(img)
        cv2.namedWindow('Video', cv2.WINDOW_FREERATIO)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
        for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
            matches = face_recognition.compare_faces(self.encoded_face_train, encode_face)
            faceDist = face_recognition.face_distance(self.encoded_face_train, encode_face)
            matchIndex = np.argmin(faceDist)
            if matches[matchIndex]:
                its = self.its[matchIndex].upper().lower()
                data = [x for x in invitees_list if x["ejamaat"] == str(its)]
                if(len(data)>=0):
                    data = data[0]
                    name = data["name"]
                    seat = data["seat"]
                    y1, x2, y2, x1 = faceloc
                    # since we scaled down by 4 times
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name+f"\n{seat}", (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    self.speak(name, seat)
            else:
                name = "guest"
                y1, x2, y2, x1 = faceloc
                # since we scaled down by 4 times
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                self.engine.say(f"Welcome {name} to 20 years plan event. Thank you!")
                self.engine.runAndWait()
        ret, jpg = cv2.imencode('.jpg', img)
        return jpg.tobytes()
