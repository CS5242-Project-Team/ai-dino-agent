import keyboard
from PIL import Image
import numpy as np
from mss import mss
import pyautogui
import os

from model_architectures import *

# -------------------------- CONFIG ---------------------------
IMAGE_SIZE = 32

# ARCHITECTURE = 'mlp'
# ARCHITECTURE = 'cnn'
ARCHITECTURE = 'rnn'
# ARCHITECTURE = 'ann'

# BINARY_MODEL_NAME = 'mlp.pt'
# BINARY_MODEL_NAME = 'cnn.pt'
# BINARY_MODEL_NAME = 'banana_v1.pt'
BINARY_MODEL_NAME = 'vanilla_rnn_v2.pt'

# MODEL = MLP()
# MODEL = LeNet5_convnet()
# MODEL = Banana()
MODEL = VanillaRNN(input_size=IMAGE_SIZE*IMAGE_SIZE)
# -------------------------- END CONFIG ---------------------------

WIDTH, HEIGHT = pyautogui.size()
BINARY_MODEL_PATH = os.path.join('binary_models', BINARY_MODEL_NAME)


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


def get_prediction(X):
    if ARCHITECTURE == 'mlp':
        X = X.view(1, -1).float()
        return net(X)
    elif ARCHITECTURE == 'cnn':
        X = X.view(1, 1, IMAGE_SIZE, IMAGE_SIZE).float()
        return net(X)
    elif ARCHITECTURE == 'rnn':
        X = X.view(-1, 1, IMAGE_SIZE * IMAGE_SIZE).float()
        h = torch.zeros(1, 1, IMAGE_SIZE * IMAGE_SIZE).float()
        scores, _ = net(X, h)
        return scores
    elif ARCHITECTURE == 'ann':
        pass


if __name__ == '__main__':
    ss_manager = mss()
    frame = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGHT}

    # Load model
    net = MODEL
    net.load_state_dict(torch.load(BINARY_MODEL_PATH, map_location=torch.device('cpu')))
    net.eval()

    while True:
        # Grab screenshot
        ss = ss_manager.grab(frame)
        image = Image.frombytes("RGB", ss.size, ss.rgb)
        grey_image = image.convert("L")
        transformed_image = process_image(grey_image)

        # Predict
        X = torch.from_numpy(transformed_image)
        prediction = get_prediction(X)
        result = np.argmax(prediction.detach().numpy())

        # Take action
        if result == 0:  # go right
            print("right")
        elif result == 1:  # go up
            up()
            print("up")
        print("--------------------------")
