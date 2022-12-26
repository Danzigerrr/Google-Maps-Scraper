"""
This program allows making random moves with the mouse. Thanks to that the PC will not sleep or shut down.
"""

import time
import random
import pyautogui


if __name__ == "__main__":
    doForMinutes = 100
    minutesUntilNextMove = 10

    for i in range(doForMinutes):
        x = random.randint(100, 1000)
        y = random.randint(100, 1000)
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(minutesUntilNextMove*60)
