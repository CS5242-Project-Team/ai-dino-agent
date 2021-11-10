import keyboard
from PIL import Image
import numpy as np
from mss import mss
import torch
import pyautogui
import os

from model_architectures import MLP, LeNet5_convnet

# -------------------------- CONFIG ---------------------------
BINARY_MODEL_NAME = 'mlp.pt'

IMAGE_SIZE = 255
# -------------------------- END CONFIG ---------------------------

WIDTH, HEIGHT = pyautogui.size()
BINARY_MODEL_PATH = os.path.join('binary_models', BINARY_MODEL_NAME)


# Assign model
def get_model():
    # model = MLP()
    model = LeNet5_convnet()

    return model


# Image transformations
def process_image(image):
    # Resize image
    new_size = (1366, 768)
    image_data = image.resize(new_size)

    # Crop image
    crop_size = (0, 150, 500, 500)
    image_data = image_data.crop(crop_size)

    new_size = (IMAGE_SIZE, IMAGE_SIZE)
    image_data = image_data.resize(new_size)
    image_data = np.array(image_data.resize(new_size))

    return image_data


# A function for go up in the game
def up():
    keyboard.press_and_release(keyboard.KEY_UP)


if __name__ == '__main__':
    ss_manager = mss()
    frame = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGHT}

    net = get_model()
    net.load_state_dict(torch.load(BINARY_MODEL_PATH, map_location=torch.device('cpu')))
    net.eval()

    while True:
        # Grab screenshot
        ss = ss_manager.grab(frame)
        image = Image.frombytes("RGB", ss.size, ss.rgb)
        grey_image = image.convert("L")
        transformed_image = process_image(grey_image)

        X = torch.from_numpy(transformed_image)
        X = X.view(1, -1)
        X = X.float()

        prediction = net(X)

        result = np.argmax(prediction.detach().numpy())
        print(result)
        print("--------------------------")

        if result == 0:  # go right
            print("right")
        elif result == 1:  # go up
            up()
            print("up")
