import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

def stackImages(scale, imgArray):
# stack images in matrix way - upper row sets the number of columns, rest of the rows can have less columns
# e.g. [[A, A, A, A], [B], [C, C, C], [D, D]]
    rows = len(imgArray)
    cols = len(imgArray[0])
    for x in range(0,rows):
        for y in range(0,len(imgArray[x])):
            if len(imgArray[x][y].shape)==2:
                imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
            if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0,0), fx=scale, fy=scale)
            else:
                imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), fx=scale, fy=scale)
            if y == 0:
                horiz = imgArray[x][y]
            else:
                horiz = np.hstack((horiz, imgArray[x][y]))
        if len(imgArray[x]) < cols and y < len(imgArray[x]):
            blank = np.zeros((imgArray[0][0].shape[0], imgArray[0][0].shape[1], 3), np.uint8)
            for i in range(0, cols - len(imgArray[x])):
                horiz = np.hstack((horiz, blank))
        if x == 0:
            vertic = horiz
        else:
            vertic = np.vstack((vertic, horiz))

    return vertic


def getContours(img, imgRes):
# get upper midpoint of bouding rectangle of the shape
    countours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in countours:
        area = cv2.contourArea(cnt)
        if area > 500:
#            cv2.drawContours(imgRes, cnt, -1, (255,0,0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def drawOnCanvas(imgRes, myPoints):
    # myPoints - list of [x, y, [B, G ,R]]
    for point in myPoints:
        cv2.circle(imgRes, (point[0], point[1]), 10, point[2], cv2.FILLED)


def findColor(img, imgRes, myColor):
# find color in the camera image and make color point
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    for color in myColor:
        lower = np.array(color[:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask, imgRes)
        cv2.circle(imgRes, (x,y), 10, color[6:], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x, y, color[6:]])
#        cv2.imshow(str(color[6])+' '+str(color[7])+' '+str(color[8]), mask)
    return newPoints


def dummy(a):
    pass


def pickColor():
# pick color by moving Track Bars, then press N to save color and go to next color,
# or press Q to save color and quit picking
    cap = cv2.VideoCapture(0)
    frameWidth = 640
    frameHeigth = 480
    brightness = 100
    cap.set(3, frameWidth)
    cap.set(4, frameHeigth)
    cap.set(10, brightness)

    colors = []

    cv2.namedWindow('TrackBars')
    cv2.resizeWindow('TrackBars', 640, 240)
    cv2.createTrackbar('Hue min', 'TrackBars', 0, 179, dummy)
    cv2.createTrackbar('Hue max', 'TrackBars', 179, 179, dummy)
    cv2.createTrackbar('Sat min', 'TrackBars', 0, 255, dummy)
    cv2.createTrackbar('Sat max', 'TrackBars', 255, 255, dummy)
    cv2.createTrackbar('Val min', 'TrackBars', 0, 255, dummy)
    cv2.createTrackbar('Val max', 'TrackBars', 255, 255, dummy)

    while True:
        success, imgWeb = cap.read()
        imgWebHSV = cv2.cvtColor(imgWeb, cv2.COLOR_BGR2HSV)
        h_min = cv2.getTrackbarPos('Hue min', 'TrackBars')
        h_max = cv2.getTrackbarPos('Hue max', 'TrackBars')
        s_min = cv2.getTrackbarPos('Sat min', 'TrackBars')
        s_max = cv2.getTrackbarPos('Sat max', 'TrackBars')
        v_min = cv2.getTrackbarPos('Val min', 'TrackBars')
        v_max = cv2.getTrackbarPos('Val max', 'TrackBars')
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(imgWebHSV, lower, upper)
        imgmask = cv2.bitwise_and(imgWeb, imgWeb, mask=mask)
        imgStack = stackImages(.6, [[imgWeb, imgWebHSV],[mask, imgmask]])
        colorWindowName = 'Pick color by moving bars (make everything else black), press N for next color, Q to quit'
        cv2.imshow(colorWindowName, imgStack)

        ch = cv2.waitKey(1)
        if ch == ord('s'):
            b_val, g_val, r_val = defineColor(imgmask)
            colors.append([h_min, s_min, v_min, h_max, s_max, v_max, b_val, g_val, r_val])
            cv2.rectangle(imgWeb, (0,200), (imgWeb.shape[1], 300), (0, 255, 0), cv2.FILLED)
            cv2.putText(imgWeb, 'Color Saved', (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
            cv2.imshow(colorWindowName, imgWeb)
            cv2.waitKey(500)
        elif ch == ord('q'):
            # b_val, g_val, r_val = defineColor(imgmask)
            # colors.append([h_min, s_min, v_min, h_max, s_max, v_max, b_val, g_val, r_val])
            # cv2.rectangle(imgWeb, (0,200), (imgWeb.shape[1], 300), (0, 255, 0), cv2.FILLED)
            # cv2.putText(imgWeb, 'Color Saved', (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
            # cv2.imshow(colorWindowName, imgWeb)
            # cv2.waitKey(500)
            break

    cap.release()
    cv2.destroyAllWindows()

    return colors


def defineColor(img):
# define BGR values of picked color
    mod_img = cv2.resize(img, (640,480))
    mod_img = mod_img.reshape(mod_img.shape[0]*mod_img.shape[1], 3)
    classificator = KMeans(n_clusters=2)
    labels = classificator.fit_predict(mod_img)
    cnt = Counter(labels)
    b, g, r = 255, 255, 255
    colorfound = classificator.cluster_centers_
    for col in colorfound:
        col[0], col[1], col[2] = int(round(col[0])), int(round(col[1])), int(round(col[2]))
        if (col != 0).all():
            b, g, r = int(col[0]), int(col[1]), int(col[2])
    return b, g, r
