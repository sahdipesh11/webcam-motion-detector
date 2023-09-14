import cv2
import time

video = cv2.VideoCapture(1)
# Wait 1 second for the camera to load
time.sleep(1)

first_frame = None
while True:
    check, frame = video.read()
    # Convert the frame to gray color and then blur.
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Assign a variable to the first frame
    if first_frame is None:
        first_frame = gray_frame_gau

    # Get the difference
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Classify deltaframe pixels (pixels with 30 or higher to 255)
    thresh_frame = cv2.threshold(delta_frame, 80, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    # Detect contours around white areas
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the contour that is out of the ordinary
    for contour in contours:
        if cv2.contourArea(contour) < 3000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    # Press the q button to stop the program.
    if key == ord("q"):
        break

video.release()
