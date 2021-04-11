import cv2
import numpy as np

class VideoCamera(object):#VIDEO CAMERA FUNCTION OF POLYGON SHAPE DETECTION MODULE


    def __init__(self):
        self.video=cv2.VideoCapture(0)

    def __del__(self):
        self.video.releast()

    def get_frame(self):
        ret,img_feed=self.video.read()

        cv2.normalize(img_feed, img_feed, 0,450, cv2.NORM_MINMAX)  # INCREASE BRIGHTNESS

        imgG = cv2.cvtColor(img_feed, cv2.COLOR_BGR2GRAY)  # image color settings

        ret, thrash = cv2.threshold(imgG, 240, 255, cv2.CHAIN_APPROX_NONE)
        contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # contour variables

        # polygon names are color-coded, outlines are in black
        for c in contours:  # getting the Contours FOR loop
            if cv2.contourArea(
                    c) > 100:  # area checker, too small object detect wont be shown, decreases clutter and false positives

                estimate = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True),
                                            True)  # pretrained cv2 model aproxmiating polygon from vertices
                cv2.drawContours(img_feed, [estimate], 0, (0, 0, 0), 5)  # drawing the Contours(outlines are in black)
                x = estimate.ravel()[0]  # x, y coordinates of detected shape
                y = estimate.ravel()[1] - 5

                # estimate = vertices, to line up to approximiated polygon
                if len(estimate) == 3:  # determing if shape is triangle
                    cv2.putText(img_feed, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))

                elif len(estimate) == 4:  # determing if shape is square OR rectangle
                    x, y, w, h = cv2.boundingRect(estimate)  # quadrilateral detecting
                    a_r = float(w) / h  # width/height = aspect ratio

                    if a_r >= 0.95 and a_r < 1.05:  # aspect ratios that are closer to 1 will be a square; 0.5 +/- tolerance between 1
                        cv2.putText(img_feed, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))

                    else:
                        cv2.putText(img_feed, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))

                elif len(estimate) == 5:  # determing if shape is pentagon
                    cv2.putText(img_feed, "pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (128, 0, 128))

                elif len(estimate) == 6:  # determing if shape is hexagon
                    cv2.putText(img_feed, "hexagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 128, 128))

                elif len(estimate) == 7:  # determing if shape is heptagon/septagon
                    cv2.putText(img_feed, "heptagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (75, 0, 130))

                elif len(estimate) == 8:  # determing if shape is octagon
                    cv2.putText(img_feed, "octagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 69, 0))

                elif len(estimate) == 9:  # determing if shape is nonagon/enneagon
                    cv2.putText(img_feed, "nonagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (210, 105, 30))

                elif len(estimate) == 10:  # determing if shape is STAR
                    cv2.putText(img_feed, "star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0))

                else:  # nothing else that fits the conditions are determined to be a circle or oval like properties
                    # variables for circle detection
                    area_c = cv2.contourArea(c)
                    perimeter_c = cv2.arcLength(c, True)
                    diameter_c = np.sqrt(4 * area_c / np.pi)
                    circle_pi = perimeter_c / diameter_c
                    print(circle_pi)  # 3.14159265359

                    if circle_pi >= 3.09 and circle_pi < 3.19:  # +/-0.5 tolerance 3.09 ->3.14(PI) <- 3.19
                        cv2.putText(img_feed, "circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 192, 203))
                        print("YOOOOOOOOOOOOOOOOOO, WE GOT A CIRCLE: ", circle_pi)

                    else:  # oval or 11+ vertice shape detected, false positive, too small ,etc.
                        buffer = 1 + 2  # nothing


        ret,jpeg=cv2.imencode('.jpg',img_feed)
        return jpeg.tobytes()