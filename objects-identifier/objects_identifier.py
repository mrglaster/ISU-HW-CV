import zmq
import cv2
import numpy as np

address = "tcp://192.168.0.100:6556"
wind_name = "Camera"
AREA_LIMIT_MIN = 40
AREA_LIMIT_MAX = 50
CAM_W_NAME = 'Camera'
BG_W_NAME = 'Thresh'

flimit = 70
slimit = 45


def fupdate(value):
    global flimit
    flimit = value


def supdate(value):
    global slimit
    slimit = value


def classify_object(contour):
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    area = cv2.contourArea(approx)

    x, y, w, h = cv2.boundingRect(approx)
    bounding_box_area = w * h
    filling_factor = area / bounding_box_area

    if filling_factor < 0.2 or filling_factor > 0.68:
        return "Circle", f"{filling_factor}"
    return "Square", f"{filling_factor}"


def identify_objects():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect("tcp://192.168.0.105:6556")

    cv2.namedWindow("Camera")
    cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)

    cv2.createTrackbar("F", "Mask", flimit, 255, fupdate)
    cv2.createTrackbar("S", "Mask", slimit, 255, supdate)

    cv2.setTrackbarPos("F", "Mask", flimit)
    cv2.setTrackbarPos("S", "Mask", slimit)

    while True:
        buffer = socket.recv()
        arr = np.frombuffer(buffer, np.uint8)
        frame = cv2.imdecode(arr, -1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        edges = cv2.Canny(gray, flimit, slimit)

        mask = cv2.dilate(edges, None, iterations=4)
        _, labeled = cv2.connectedComponents(mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            object_type, circularity = classify_object(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{object_type}({circularity})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                        2)

        cv2.putText(frame, f"Objects detected: {len(contours)}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0))

        cv2.imshow("Camera", frame)
        cv2.imshow("Mask", mask)

        key = cv2.waitKey(500)
        if key == ord("q"):
            break


if __name__ == '__main__':
    identify_objects()
