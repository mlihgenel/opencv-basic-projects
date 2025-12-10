import cv2

def ask_for_tracking_api():
    print('Which Tracker API do you wanna use?')
    print('1 - MIL Tracker')
    print('2 - KCF Tracker')

    choice = int(input('Please select your tracker : '))

    if choice == 1:
        tracker = cv2.TrackerMIL_create()
        return tracker
    elif choice == 2:
        tracker = cv2.TrackerKCF_create()
        return tracker
    else:
        print('Invalid choice. Closing...')
        quit()
        

tracker = ask_for_tracking_api()
tracker_name = str(tracker).split()[1].split('.')[1]

cap = cv2.VideoCapture('sample_video.mp4')
tracking = False  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if tracking:
        success, roi = tracker.update(frame)
        (x, y, w, h) = tuple(map(int, roi))

        if success:
            p1 = (x, y)
            p2 = (x + w, y + h)
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 5)
            cv2.putText(frame, tracker_name + " is tracking", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
        else:
            cv2.putText(frame, "Tracking Failure", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)

    else:
        cv2.putText(frame, "Press 's' to select ROI", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 4)
        cv2.putText(frame, "After select ROI press Enter button", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 4)

    
    cv2.imshow("Tracking", frame)

    
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and not tracking:
        roi = cv2.selectROI("Tracking", frame, False, False)
        tracker.init(frame, roi)
        tracking = True

    elif key == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()


