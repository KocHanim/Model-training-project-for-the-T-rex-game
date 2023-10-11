#to import the model in json format that we have trained
from keras.models import model_from_json
import numpy as np 
from PIL import Image
import keyboard
import time
#on-screen logging library
from mss import mss

# Specify coordinates and dimensions to capture a specific area from the screen
mon = {"top": 500, "left": 720, "width": 250, "height": 100}
# mss library will take the screenshot using the specified coordinates
sct = mss()

# Specify image dimensions
width = 125
height = 50

# Starting functions that prepare the image for the model to make predictions

# Loading the model - Load the model and its weights in JSON format
model = model_from_json(open("model_new.json", "r").read())
model.load_weights("trex_weight_new.h5")

# Determining the labels of predictions
labels = ["Down", "Right", "Up"]

# Initialising time variables for FPS (Time Per Frame) calculation
framerate_time = time.time()
counter = 0
i = 0

# Setting the dwell time after key press operation
delay = 0.4
key_down_pressed = False

# Start an infinite loop (the programme runs until closed by the user)
while True:
    # Capturing a screenshot
    img = sct.grab(mon)
    im = Image.frombytes("RGB", img.size, img.rgb)
    im2 = np.array(im.convert("L").resize((width, height)))  # Converting and resizing the image to black and white
    im2 = im2 / 255  # Normalisation (scaling between 0 and 1)

    # Translate the image into a sequence that the model can understand
    X = np.array([im2])
    X = X.reshape(X.shape[0], width, height, 1)

    # Forecasting with the model
    r = model.predict(X)
    result = np.argmax(r)

    # Key presses according to model prediction
    if result == 0:  # down=0
        keyboard.press(keyboard.KEY_DOWN)
        key_down_pressed = True
    elif result == 2:  # up = 2
        if key_down_pressed:
            keyboard.release(keyboard.KEY_DOWN)
        time.sleep(delay)
        keyboard.press(keyboard.KEY_UP)
        if i < 1500:  # Speeding up after the 1500th frame
            time.sleep(0.3)
        elif 1500 < i < 5000:
            time.sleep(0.2)
        else:
            time.sleep(0.17)
        keyboard.press(keyboard.KEY_UP)
        keyboard.release(keyboard.KEY_DOWN)

    # FPS (Time Per Frame) calculation and necessary adjustments
    counter += 1
    if (time.time() - framerate_time) > 1:
        counter = 0
        framerate_time = time.time()
        if i <= 1500:
            delay -= 0.003
        else:
            delay -= 0.005
        if delay < 0:
            delay = 0

        # Printing model prediction results to the screen
        print("--------------------------------------")
        print("Down: {} \nRight: {} \nUp: {} \n".format(r[0][0], r[0][1], r[0][2]))
        i += 1

             
             
             
             
             


















