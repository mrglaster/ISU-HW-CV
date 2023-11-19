import numpy as np
import os.path
import cv2

CORRECT_NUMBERS = [0, 1, 1, 2, 2, 3, 3, 1, 2, 2, 3, 1]
LOWER_BORDER = 280000
UPPER_BORDER = 380000


def get_pencils(image_path):
    original = cv2.imread(image_path)
    gray_im = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    gray_correct = np.array(255 * (gray_im / 255) ** 1.2, dtype='uint8')
    thresh = cv2.adaptiveThreshold(gray_correct, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 11)
    thresh = cv2.bitwise_not(thresh)
    kernel = np.ones((15, 15), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    img_erode = cv2.erode(img_dilation, kernel,
                          iterations=1)
    ret, labels = cv2.connectedComponents(img_erode)
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0
    contours, _ = cv2.findContours(img_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntr = 0
    for i in contours:
        area = cv2.contourArea(i)
        if LOWER_BORDER < area < UPPER_BORDER:
            cntr += 1
    return cntr


def process_images():
    pens_general = 0
    for i in range(12):
        path = f'images/img ({i + 1}).jpg'
        pens = get_pencils(path)
        if pens == CORRECT_NUMBERS[i]:
            print(f"Found in {os.path.basename(path)} : {pens}")
            pens_general += pens
        else:
            raise ValueError(f"File {os.path.basename(path)}, Got: {pens}, Expected: {CORRECT_NUMBERS[i]}")
    print('\n' + '=' * 40 + f'\nTOTAL: {pens_general}')


def main():
    process_images()


if __name__ == '__main__':
    main()
