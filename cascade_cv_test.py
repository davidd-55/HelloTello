import cascade_importer as ci
import cv2
import numpy as np 


def facedetect(img, cascade):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        x_center = int(x + (w/2))
        y_center = int(y + (h/2))
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
        cv2.circle(img, (x_center, y_center), 10, (255, 0, 0), 1)

        # print(x_center, ", ", y_center)

    cv2.imshow('stream', img)


if __name__ == "__main__":

    cas_lst = ci.cascade_finder()
    print("Available libraries:")
    for cascade in cas_lst:
        print(cascade)
    
    cascade_dir = "cascades/" + ci.usr_choice(cas_lst)
    cascade = cv2.CascadeClassifier(cascade_dir)
    stream = cv2.VideoCapture(0)

    while True:
        ret, frame = stream.read()

        if frame is None:
            print("No video data found. Try again.")
            exit()

        facedetect(frame, cascade)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
