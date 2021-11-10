import os
from PIL import Image
import PIL.ImageOps as ops

# Directory declarations
data_dir = '/content/drive/MyDrive/CS5242/Data'

data_labels = ['jump', 'inaction']
cleaned_data_dir = os.path.join(data_dir, 'cleaned_data')
processed_data_dir = os.path.join(data_dir, 'processed_data')

# Initializations
processed_image_objects = []
processed_image_names = []

def create_folders():
  for label in data_labels:
    processed_data_label_dir = os.path.join(processed_data_dir, label)
    os.makedirs(processed_data_label_dir) if not os.path.exists(processed_data_label_dir) else None


def process_images():
    for label in data_labels:
        print("")
        print("Processing {}...".format(label))
        dir = os.path.join(cleaned_data_dir, label)
        dir_items = os.listdir(dir)

        for ind, image_name in enumerate(dir_items):
            if ind % 50 == 0:
                print("Progress: {:.3}%".format(100 * ind / len(dir_items)))

            image_path = os.path.join(dir, image_name)
            image_data = Image.open(image_path).convert('L')  # open and covert to grayscale

            # Resize image
            new_size = (1366, 768)
            image_data = image_data.resize(new_size)

            # Crop image
            crop_size = (0, 150, 500, 500)
            image_data = image_data.crop(crop_size)

            # Create inverted image
            inverted_image_data = ops.invert(image_data)

            # Create new image names
            image_name_without_ext = image_name.split('.')[0]
            processed_image_names.append(
                os.path.join(processed_data_dir, label, '{}_{}.jpg'.format(image_name_without_ext, 0)))
            processed_image_names.append(
                os.path.join(processed_data_dir, label, '{}_{}.jpg'.format(image_name_without_ext, 1)))

            # Append new images to collection
            processed_image_objects.append(image_data)
            processed_image_objects.append(inverted_image_data)


def save_images():
  print("Saving images...")
  for ind, processed_image in enumerate(processed_image_objects):
    if ind % 100 == 0:
      print("Progress: {:.3}%".format(100 * ind/len(processed_image_objects)))

    processed_image.save(processed_image_names[ind])

# Main Function
create_folders()
process_images()
save_images()