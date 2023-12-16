import os
import cv2
import numpy as np
from skimage.measure import label


def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=30, maxRadius=59
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        cntr = 0
        for j in circles[0, :]:
            cntr += 1
        try:
            b_frame = np.mean(frame, axis=2)
            if cntr == 1 and np.max(label(b_frame)) == 30116:
                return True
        except:
            pass
    return False


def main():
    video_capture = cv2.VideoCapture("output.avi")
    cntr = 0
    images = []
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        status = process_frame(frame)
        if status:
            cntr += 1
            images.append(frame)
        cv2.imshow("Video Frame", frame)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    for i in images:
        cv2.imshow("This image is MINE!", i)
        if cv2.waitKey(500) & 0xFF == ord('q'):
            break
    print(f"My image has been shown shown: {cntr} times")


if __name__ == "__main__":
    main()
