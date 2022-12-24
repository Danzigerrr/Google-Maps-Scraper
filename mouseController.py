import time
import random
# a module which has functions related to time.
# It can be installed using cmd command:
# pip install time, in the same way as pyautogui.
import pyautogui

for i in range(100):
    x = random.randint(100, 1000)
    y = random.randint(100, 1000)
    pyautogui.moveTo(x, y, duration=1)
    time.sleep(60)
