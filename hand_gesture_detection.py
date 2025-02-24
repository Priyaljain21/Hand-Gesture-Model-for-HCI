
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model              # type: ignore
import pyautogui


n = int(input("Enter Choice - "))

if n==1:
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils

    model = load_model(r'C:\Users\DELL\OneDrive\Desktop\mp_hand_gesture')

    f = open(r'C:\Users\DELL\OneDrive\Desktop\gesture.names', 'r')
    classNames = f.read().split('\n')
    f.close()
    print(classNames)


    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()

        x, y, c = frame.shape

        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(framergb)

        
        className = ''

        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                prediction = model.predict([landmarks])
                classID = np.argmax(prediction)
                className = classNames[classID]

        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0,0,255), 2, cv2.LINE_AA)

        cv2.imshow("Output", frame) 

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()

    cv2.destroyAllWindows()
elif n==2:
    capture_hand = mp.solutions.hands.Hands()
    drawing_option = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()
    camera = cv2.VideoCapture(0)
    x1 = x2 = y1 = y2 = 0
    while True:
        _,image = camera.read()
        image_height, image_width, _ = image.shape 
        image = cv2.flip(image,1)
        rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        output_hands = capture_hand.process(rgb_image)
        all_hands = output_hands.multi_hand_landmarks
        if all_hands:
            for hand in all_hands:
                drawing_option.draw_landmarks(image,hand)
                one_hand_landmarks = hand.landmark
                for id, lm in enumerate(one_hand_landmarks):
                    x = int(lm.x * image_width)
                    y = int(lm.y * image_height)
                    #print(x,y)cv2.COLOR_BGR2RGB
                    if id == 8:
                        mouse_x = int(screen_width / image_width * x)
                        mouse_y = int(screen_height/image_height *y)
                        cv2.circle(image,(x,y),10,(0,255,255))
                        pyautogui.moveTo(mouse_x,mouse_y)
                        x1 = x
                        y1 = y
                    if id == 4:
                        x2 = x
                        y2 = y
                        cv2.circle(image,(x,y),10,(0,255,255))
            dist = y2 - y1 
            print(dist)
            if(dist<20):
                pyautogui.click()        
                    
        cv2.imshow("Hand movement video capture", image)
        if cv2.waitKey(1) == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
