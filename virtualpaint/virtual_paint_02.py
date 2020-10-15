# Virtual Paint
#
# - pick colors by moving track bars (everything else should be black in bottom-right image)
#   - press S to define save color
#   - press Q to quit picking color
# - have fun drawing ;-)
#

import cv2
import numpy as np
from .virtual_paint_library_02 import findColor, drawOnCanvas, defineColor

class VirtualPaint02(object):

    def __init__(self):
        frameWidth = 640
        frameHeight = 480
        brightness = 100
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, frameWidth)
        self.cam.set(4, frameHeight)
        self.cam.set(10, brightness)
        self.myPoints = []
        self.chosenColors = []

    def __del__(self):
        self.cam.release()

    def collectColors(self, colorsfromDB):
        colorscollection = []
        for col in colorsfromDB:
            colorscollection.append([col.huemin, col.satmin, col.valmin,
                                     col.huemax, col.satmax, col.valmax,
                                     col.B, col.G, col.R])
        self.chosenColors = colorscollection

    def get_frame(self):
        # myPoints = [] # [x, y, [colorB, colorG, colorR]]
        # chosenColors = pickColor()

        success, imgWebflip = self.cam.read()
        imgWeb = cv2.flip(imgWebflip, 1)
        imgResult = imgWeb.copy()

        newPoints = []

        if self.chosenColors == []:
            pass
            # print('No colors selected.')
        else:
            newPoints = findColor(imgWeb, imgResult, self.chosenColors)
        if len(newPoints) != 0:
            for newP in newPoints:
                self.myPoints.append(newP)
        if len(self.myPoints) != 0:
            drawOnCanvas(imgResult, self.myPoints)

        # imgWeb = imgResult
        # keypressed = cv2.waitKey(1)
        # if keypressed == ord('s'):
        #     print('saved')
        #     cv2.rectangle(imgWeb, (0,200), (imgWeb.shape[1], 300), (0, 255, 0), cv2.FILLED)
        #     cv2.putText(imgWeb, 'Color Saved', (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
        #     ret, jpeg = cv2.imencode('.jpg', imgWeb)
        #     cv2.waitKey(500)
        #     return jpeg.tobytes()
        # else:
        #     ret, jpeg = cv2.imencode('.jpg', imgWeb)
        #     return jpeg.tobytes()

        # return imgResult

        ret, jpeg = cv2.imencode('.jpg', imgResult)
        return jpeg.tobytes()


    def process_frame(self, imgWeb):
        one = np.ones_like(imgWeb)*50
        imgWeb += one

        ret, jpeg = cv2.imencode('.jpg', imgWeb)
        return jpeg.tobytes()


def PickColor(HSVvalues):
    frameWidth = 640
    frameHeight = 480
    brightness = 100
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, brightness)
    colors = []

    [h_min, s_min, v_min, h_max, s_max, v_max] = HSVvalues

    success, imgWeb = cap.read()
    cap.release()

    imgWebHSV = cv2.cvtColor(imgWeb, cv2.COLOR_BGR2HSV)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(imgWebHSV, lower, upper)

    imgmask = cv2.bitwise_and(imgWeb, imgWeb, mask=mask)

    # imgStack = stackImages(.6, [[imgWeb, imgWebHSV],[mask, imgmask]])

    # colorWindowName = 'Pick color by moving bars (make everything else black), press N for next color, Q to quit'
    # cv2.imshow(colorWindowName, imgStack)

    b_val, g_val, r_val = defineColor(imgmask)

    colors.append([h_min, s_min, v_min, h_max, s_max, v_max, b_val, g_val, r_val])

    # ret, jpeg = cv2.imencode('.jpg', imgmask)
    # return jpeg.tobytes()

    # keypressed = cv2.waitKey(1)
    # if keypressed == ord('s'):
    #     b_val, g_val, r_val = defineColor(imgmask)
    #     colors.append([h_min, s_min, v_min, h_max, s_max, v_max, b_val, g_val, r_val])
    #     cv2.rectangle(imgWeb, (0,200), (imgWeb.shape[1], 300), (0, 255, 0), cv2.FILLED)
    #     cv2.putText(imgWeb, 'Color Saved', (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
    #     cv2.imshow(colorWindowName, imgWeb)
    #     cv2.waitKey(500)
    # elif keypressed == ord('q'):
    #     break

    return colors
