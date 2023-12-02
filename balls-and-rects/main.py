import numpy as np
import cv2
from skimage.measure import label


def get_bbox(current_segment):
    y_min, x_min = current_segment[0][0], current_segment[1][0]
    y_max, x_max = current_segment[0][-1], current_segment[1][-1]
    return x_min, y_min, x_max, y_max


def analyse(labeled, img_hsv):
    rects = 0
    circles = 0
    shades = {}
    for lbl in range(1, np.max(labeled) + 1):
        current_segment = np.where(labeled == lbl)
        x_min, y_min, x_max, y_max = get_bbox(current_segment)
        segment_area = (x_max - x_min + 1) * (y_max - y_min + 1)
        figure_type = segment_area == len(current_segment[0])  # is rectangle
        shade = img_hsv[y_min, x_min, 0]
        shades.setdefault(shade, [0, 0])
        figure_index = int(not figure_type)
        shades[shade][figure_index] += 1
        if figure_type:
            rects += 1
        else:
            circles += 1
    return dict(sorted(shades.items())), rects, circles


def process_image(path):
    image = cv2.imread(path)
    im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    _, thresh = cv2.threshold(im_gray, 128, 192, cv2.THRESH_OTSU)
    labeled = label(thresh)
    shades, rects, circles = analyse(labeled, img_hsv)
    print(f"Figures found: {np.max(labeled)}")
    print(f"Rectangles: {rects}")
    print(f"Circles: {circles}")
    print(f"Shades: {len(shades)}")
    print('\nShade    Rectangles    Circles')
    for i in shades:
        print(f"{i}         {shades[i][0]}          {shades[i][1]}")

def main():
    image_path = "balls_and_rects.png"
    process_image(image_path)

if __name__ == "__main__":
    main()
    
