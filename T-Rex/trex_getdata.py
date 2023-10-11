import keyboard
import uuid  # To capture the screen
import time
from PIL import Image  # Python image library
from mss import mss

"""
https://fivesjs.skipser.com/trex-game/
"""
monitor = {"top": 500, "left": 720, "width": 250, "height": 100}
# The 'mss' library captures a specific area of the screen by using a dictionary of pixels to create a frame

sct = mss()

i = 0

def record_screen(record_id, key):
    global i
    i += 1
    print("{}: {}".format(key, i))
    img = sct.grab(monitor)
    img = Image.frombytes("RGB", img.size, img.rgb)
    img.save("./img/{}_{}_{}.png".format(key, record_id, i))

is_exit = False

def exit():
    global is_exit
    is_exit = True

keyboard.add_hotkey("esc", exit)

record_id = uuid.uuid4()

while True:
    if is_exit:
        break

    try:
        if keyboard.is_pressed(keyboard.KEY_UP):
            record_screen(record_id, "up")
            time.sleep(0.1)
        elif keyboard.is_pressed(keyboard.KEY_DOWN):
            record_screen(record_id, "down")
            time.sleep(0.1)
            # For places where it should not jump or crouch
        elif keyboard.is_pressed("right"):
            record_screen(record_id, "right")
            time.sleep(0.1)
    except RuntimeError:
        continue
