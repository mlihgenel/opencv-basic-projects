import cv2
import os 


def add_user():
    face_classifier = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')
    
    def face_crop(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None
        for (x,y,w,h) in faces:
            cropped_face = img[y-100:y+h+100, x-100:x+w+100]
            
        return cropped_face
    
    cap = cv2.VideoCapture(0)
    img_id = 0 
    username = input("Kaydedilecek kişinin ismini girin: ").strip()
    folder_path = f"user_face_dataset/{username}"
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cropped = face_crop(frame)
        if  cropped is not None:
            img_id += 1
            face = cv2.resize(cropped, (600,600))
            
            k = cv2.waitKey(1)
            if k == ord('p'):
                file_path = f"{folder_path}/data.{str(img_id)}.jpg"
                cv2.imwrite(file_path, face)
                print("Image saved...")
            
            if  k == 27 or k == ord('q'):
                break
            
            cv2.imshow("Detect Face", face)


    cap.release()
    cv2.destroyAllWindows()
