import cv2
import time
from emailing import send_email
import glob
import os
from threading import Thread

video = cv2.VideoCapture(1)
# Wait 1 second for the camera to load
time.sleep(1)

first_frame = None
status_list = []
count = 1


# Delete all images of images folder
def clean_folder():
    print("clean_folder function started.")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean_folder function end.")


while True:
    status = 0
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
    thresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    # Detect contours around white areas
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the contour that is out of the ordinary
    for contour in contours:
        if cv2.contourArea(contour) < 7000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            # Get the image that is in the middle of the list
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        # Create threads for send_email and clean_folder functions

        email_thread = Thread(target=send_email, args=(image_with_object, ))
        # Process email_thread in the background
        email_thread.daemon = True

        # Delete all images in the folder after sending an email
        clean_thread = Thread(target=clean_folder)
        email_thread.daemon = True

        email_thread.start()

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    # Press the q button to stop the program.
    if key == ord("q"):
        break

video.release()

clean_thread.start()
