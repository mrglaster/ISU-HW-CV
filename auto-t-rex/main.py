import time
import webbrowser

import cv2
import numpy as np
import pyautogui

LOWER_JUMP_BORDER = 900
UPPER_JUMP_BORDER = 7000
pyautogui.PAUSE = 0.005


def start_game():
    trex_url = "https://chromedino.com/"
    webbrowser.open(trex_url)
    time.sleep(5)
    pyautogui.press('space')


def process_bot_ai():
    while True:
        current_screen = pyautogui.screenshot(region=(735, 220, 160, 180))
        current_screen = cv2.cvtColor(np.array(current_screen), cv2.COLOR_RGB2BGR)
        black_pixels = np.sum(current_screen < 100)
        white_pixels = np.sum(current_screen > 100)
        print(black_pixels)
        if LOWER_JUMP_BORDER < black_pixels < UPPER_JUMP_BORDER:
            pyautogui.press('up')

        # if LOWER_JUMP_BORDER < white_pixels < UPPER_JUMP_BORDER:
        #     pyautogui.press('up')


def process_game():
    start_game()
    process_bot_ai()


def main():
    process_game()


if __name__ == "__main__":
    main()
