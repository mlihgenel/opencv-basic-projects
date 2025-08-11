
import face_recognition
import os, sys
import cv2
import numpy as np 
from datetime import datetime

class FaceRecognition():
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    procces_current_frame = True
    DATASET_DIR = "user_face_dataset"
    
    def __init__(self):
        self.encode_faces()
        self.logged_names = set()
        
    def encode_faces(self):
        for name in os.listdir(self.DATASET_DIR): #user_face_dateset
            name_dir = os.path.join(self.DATASET_DIR, name)#user_face_dateset/melih/
            for image in os.listdir(name_dir): #user_face_dateset/melih/data.*.jpg
                face_images = face_recognition.load_image_file(os.path.join(name_dir, image))
                face_encodings = face_recognition.face_encodings(face_images)[0]
                
                self.known_face_encodings.append(face_encodings)
                self.known_face_names.append(name)
                     
    def recognation(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Kamera Bulunamadı...")
            sys.exit()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break 
            
            if self.procces_current_frame:
                small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
                code = cv2.COLOR_BGR2RGB
                rgb_small_frame = cv2.cvtColor(small_frame, code)
                
                
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
                
                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = 'Unknown'
                    
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_matches_index = np.argmin(face_distances)
                    
                    if matches[best_matches_index]:
                        name = self.known_face_names[best_matches_index]
                    


                    self.face_names.append(f'{name}')
                self.attendance(name)
                                      
            self.procces_current_frame = not self.procces_current_frame
            
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                cv2.rectangle(frame, (left,top), (right,bottom), (0,0,255), 1)
                cv2.rectangle(frame, (left, bottom), (right, bottom + 40), (0,0,255), -1)
                cv2.putText(frame, name, (left, bottom+27), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
                
            cv2.imshow('Face Recognation', frame)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break
        
        print("============================")
        if name == 'Unknown':
            print("ERİŞİM REDDEDİLDİ....")
        else:
            print("GİRİŞ BAŞARILI....")
        print("============================")
           

            
            
        cap.release()
        cv2.destroyAllWindows()
                    
    def attendance(self, name):

        if name in self.logged_names:
            return 
        
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        
        with open('access_log.csv', 'a') as f:  
            f.write(f'{date} {time}, {name}\n')
            self.logged_names.add(name)
        
