from mss import mss
import numpy as np
import pyautogui
import os

from model_architectures import *

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from PIL import Image
# -------------------------- CONFIG ---------------------------
# ARCHITECTURE = 'mlp'
ARCHITECTURE = 'cnn'
# ARCHITECTURE = 'rnn'
# ARCHITECTURE = 'ann'

if ARCHITECTURE == 'mlp':
    IMAGE_SIZE = 255
    BINARY_MODEL_NAME = 'mlp.pt'
    MODEL = MLP()

if ARCHITECTURE == 'cnn':
    IMAGE_SIZE = 51
    BINARY_MODEL_NAME = 'banana_v1.pt'
    MODEL = Banana()

if ARCHITECTURE == 'rnn':
    IMAGE_SIZE = 32
    SEQ_LENGTH = 1
    BINARY_MODEL_NAME = 'vanilla_rnn_v2.pt'
    MODEL = VanillaRNN(input_size=int(IMAGE_SIZE*IMAGE_SIZE/SEQ_LENGTH))

if ARCHITECTURE == 'ann':
    IMAGE_SIZE = 224
    BINARY_MODEL_NAME = 'ann.pt'
    MODEL = VisionANN().vision_transformer
# -------------------------- END CONFIG ---------------------------

# ----------------------------VARIABLES-----------------------------
WIDTH, HEIGHT = pyautogui.size()
BINARY_MODEL_PATH = os.path.join('binary_models', BINARY_MODEL_NAME)
GAME_ELEMENT = None
# ----------------------------END VARIABLES-------------------------


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
    # image_data.save("test.jpg")
    image_data = np.array(image_data)

    return image_data


def get_prediction(net, X):
    if ARCHITECTURE == 'mlp':
        X = X.view(1, IMAGE_SIZE, IMAGE_SIZE).float()
        return net(X)
    elif ARCHITECTURE == 'cnn':
        X = X.view(1, 1, IMAGE_SIZE, IMAGE_SIZE).float()
        return net(X)
    elif ARCHITECTURE == 'rnn':
        X = X.view(-1, SEQ_LENGTH, int(IMAGE_SIZE * IMAGE_SIZE/SEQ_LENGTH)).float()
        h = torch.zeros(1, SEQ_LENGTH, int(IMAGE_SIZE * IMAGE_SIZE/SEQ_LENGTH)).float()
        scores, _ = net(X, h)
        return scores
    elif ARCHITECTURE == 'ann':
        X = X.view(1, 1, IMAGE_SIZE, IMAGE_SIZE).float()
        return net(X)


def start_game():
    options = webdriver.ChromeOptions()
    options.add_argument("--mute-audio")
    options.add_argument('--disable-extensions')
    options.add_argument("--start-maximized")
    options.add_argument("--start-fullscreen")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])

    # create driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # get to dino game
    try:
        driver.get("chrome://dino")
    except:
        pass

    # Set game speed == 6
    driver.execute_script("Runner.config.MAX_SPEED = 6;")

    # start game
    global GAME_ELEMENT
    GAME_ELEMENT = driver.find_element_by_tag_name("body")
    GAME_ELEMENT.send_keys(Keys.SPACE)

    return driver


if __name__ == '__main__':
    # Load model
    net = MODEL
    net.load_state_dict(torch.load(BINARY_MODEL_PATH, map_location=torch.device('cpu')))
    net.eval()

    # screen capture
    ss_manager = mss()
    frame = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGHT}

    driver = start_game()

    while True:
        # Grab screenshot
        ss = ss_manager.grab(frame)
        image = Image.frombytes("RGB", ss.size, ss.rgb)
        grey_image = image.convert("L")
        transformed_image = process_image(grey_image)

        # Predict
        X = torch.from_numpy(transformed_image)
        prediction = get_prediction(net, X)
        result = np.argmax(prediction.detach().numpy())

        # Take action
        if result == 0:  # go right
            print("right")
        elif result == 1:  # go up
            GAME_ELEMENT.send_keys(Keys.SPACE)
            print("up")
        print("--------------------------")
