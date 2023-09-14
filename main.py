import cv2
import time

video = cv2.VideoCapture(1)
# Wait 1 second for the camera to load
time.sleep(1)

while True:
    check, frame = video.read()
    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)
    # Press the q button to stop the program.
    if key == ord("q"):
        break

video.release()
