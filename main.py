import cv2, cvzone, time, random
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)# width
cap.set(4, 480)# height


detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0] # [AI, Player]
global imgAI
while True:
    imgBG = cv2.imread("resources/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0,0), None, 0.7, 0.94)
    
    #Find Hands
    hands, img = detector.findHands(imgScaled)


    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)),(700, 500), cv2.FONT_HERSHEY_PLAIN, 6,(255, 0,255), 10)
            if timer>3:
                stateResult = True
                timer = 0
            if hands:
                playerMove=None
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                if fingers == [1, 1, 1, 1, 1]:
                    playerMove = 1
                if fingers == [0, 0, 0, 0, 0]:
                    playerMove = 2
                if fingers == [0, 1, 1, 0, 0]:
                    playerMove = 3
                
                randomNumber = random.randint(1, 3)
                imgAI = cv2.imread(f"resources/{randomNumber}.png", cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                #Player Wins
                if (playerMove == 1 and randomNumber == 2) or \
                   (playerMove == 2 and randomNumber == 3) or \
                   (playerMove == 3 and randomNumber == 1):
                   scores[1] += 1

                #AI Wins
                if (playerMove == 2 and randomNumber == 1) or \
                   (playerMove == 3 and randomNumber == 2) or \
                   (playerMove == 1 and randomNumber == 3):
                    scores[0] += 1
    
                


    imgBG[299:750, 914: 1362] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]),(470, 240), cv2.FONT_HERSHEY_PLAIN, 4,(255, 255,255), 6)
    cv2.putText(imgBG, str(scores[1]),(1280, 240), cv2.FONT_HERSHEY_PLAIN, 4,(255, 255,255), 6)

    #cv2.imshow("Picture",img)
    cv2.imshow("BG", imgBG)
    #cv2.imshow("Scaled", imgScaled)
    key = cv2.waitKey(1)
    if key == ord('s'):
      startGame = True
      initialTime = time.time()
      stateResult = False
