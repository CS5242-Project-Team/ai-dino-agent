import keyboard
import pyautogui
import time
import os
from threading import Lock, Thread

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

global user_id

########################################## START Config ############################################
DEBUG = True
# DEBUG = False

user = 'vignesh'
# user = 'niranjana'
# user = 'prakash'
# user = 'joes'
########################################## END Config ############################################

if user == 'vignesh':
	user_id = 1
elif user == 'niranjana':
	user_id = 2
elif user == 'prakash':
	user_id = 3
elif user == 'joes':
	user_id = 4

current_directory = os.getcwd()

directory_jump = os.path.join(current_directory, 'data', 'raw_data', 'jump')
directory_duck = os.path.join(current_directory, 'data', 'raw_data', 'duck')
directory_inaction = os.path.join(current_directory, 'data', 'raw_data', 'inaction')

directory_cleaned_jump = os.path.join(current_directory, 'data', 'cleaned_data', 'jump')
directory_cleaned_duck = os.path.join(current_directory, 'data', 'cleaned_data', 'duck')
directory_cleaned_inaction = os.path.join(current_directory, 'data', 'cleaned_data', 'inaction')

mutex = Lock()


def process_space_bar():
	mutex.acquire()
	print("space_bar") if DEBUG else None
	save_single_screenshot(pyautogui.screenshot(), directory_jump)
	time.sleep(0.5)
	mutex.release()


def process_inaction():
	print("inaction") if DEBUG else None
	save_single_screenshot(pyautogui.screenshot(), directory_inaction)


def save_single_screenshot(screenshot, directory):
	file_id = str(time.time())
	file_id = "{}_{}_{}".format(user_id, file_id.split(".")[0], file_id.split(".")[1])
	file_name = os.path.join(directory, '{}.jpg'.format(file_id))
	screenshot.save(file_name)


def create_necessary_folders():
	print("Creating necessary folders...")
	print("---")

	# create necessary data folders
	os.makedirs(directory_jump) if not os.path.exists(directory_jump) else None
	os.makedirs(directory_duck) if not os.path.exists(directory_duck) else None
	os.makedirs(directory_inaction) if not os.path.exists(directory_inaction) else None

	os.makedirs(directory_cleaned_jump) if not os.path.exists(directory_cleaned_jump) else None
	os.makedirs(directory_cleaned_duck) if not os.path.exists(directory_cleaned_duck) else None
	os.makedirs(directory_cleaned_inaction) if not os.path.exists(directory_cleaned_inaction) else None


def capture_jump_duck():
	keyboard.add_hotkey('space', lambda: process_space_bar())
	keyboard.add_hotkey(keyboard.KEY_UP, lambda: process_space_bar())
	# Keyboard waiting for input...
	print("Waiting for keyboard input...")
	keyboard.wait()


def capture_inaction():
	while True:
		mutex.acquire()
		process_inaction()
		mutex.release()
		time.sleep(0.5)


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


def main():
	print("Running data collection script...")
	print("---")
	create_necessary_folders()

	p0 = Thread(target=start_game)
	p0.daemon = True

	p1 = Thread(target=capture_jump_duck)
	p1.daemon = True

	p2 = Thread(target=capture_inaction)
	p2.daemon = True

	p0.start()
	p1.start()
	p2.start()

	p0.join(1)
	p1.join(1)
	p2.join(1)

	while True:
		time.sleep(10)


if __name__ == '__main__':
	main()
