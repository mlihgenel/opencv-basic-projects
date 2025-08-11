from face_recognation import FaceRecognition
from add_user import add_user

if __name__ == "__main__":
    
    while True:
        print("============================")
        print(" 1 - Giriş Yap")
        print(" 2 - Yeni Kullanıcı Ekle ")
        print(" 3 - Çıkış")
        print("============================")
        try:
            choice = int(input("Seçim yapınız....: "))
        except:
            print("Geçersiz seçim yapıtnız....")
            break
        
        if choice == 1:
            fr = FaceRecognition()
            rg = fr.recognation() 
            break
            
        elif choice == 2:
            add_user()
            break
        elif choice == 3:
            print("Çıkış yapılıyor...")
            break
        else:
            print("Hatalı seçim yaptınız tekrar giriniz...")