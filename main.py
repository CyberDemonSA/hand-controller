import cv2
import mediapipe as mp
from pynput.mouse import Button, Controller
import time


camera = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

mouse = Controller()

p = [0 for i in range(21)]

while True:
    good, img = camera.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for id, point in enumerate(handLms.landmark):
                width, height, color = img.shape
                width, height = int(point.x * height), int(point.y * width)
                p[id] = height

                if id == 4:
                    cv2.circle(img, (width, height), 15, (255, 8, 255), cv2.FILLED)
                    if 0 < width < 700 and 0 < height < 500:

                        width=700-width
                        driftx = 0
                        drifty = 0
                        mposx = mouse.position[0]//2.5-(width*1.2-100)
                        mposy = mouse.position[1]//2-(height*1.2-100)
                        speed = 0.8

                        if mposx < 0 and not (-8 < mposx < 8):
                            driftx = 1 * abs(mposx * speed)
                        elif mposx > 0 and not (-8 < mposx < 8):
                            driftx = -1 * abs(mposx * speed)

                        if mposy < 0 and not (-8 < mposy < 8):
                            drifty = 1 * abs(mposy * speed)
                        elif mposy > 0 and not (-8 < mposy < 8):
                            drifty = -1 * abs(mposy * speed)

                        mouse.move(driftx, drifty)

                        driftx = 0
                        drifty = 0

                    if -20 < p[8]-p[4] < 20:
                        mouse.click(Button.left, 1)
                        time.sleep(0.5)

                    if -20 < p[12]-p[4] < 20:
                        mouse.click(Button.right, 1)
                        time.sleep(0.5)


    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('q'):
        break