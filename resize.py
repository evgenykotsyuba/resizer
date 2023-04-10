import os
import cv2
import configparser
from rembg import remove

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CURRENT_DIR, 'config.ini')

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Specify the path to the master_model and result_model folders
MASTER_FOLDER = os.path.abspath(os.path.join(CURRENT_DIR, config.get('location', 'master_model')))
RESULT_FOLDER = os.path.abspath(os.path.join(CURRENT_DIR, config.get('location', 'result_model')))

# Check if the master_model or result_model folder exists, if not create it
os.makedirs(MASTER_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


def image_resize():
    try:
        # Get the file types and image size from the config file
        file_types = config.get('type', 'file_type').split(",")
        set_width = config.getint('resolution', 'width')
        set_height = config.getint('resolution', 'height')
        default_extension = config.getboolean('type', 'default_extension')
        new_extension = config.get('type', 'new_extension')

        # Loop through all the files in the master_model folder
        for filename in os.listdir(MASTER_FOLDER):
            # Check if the file is an image of one of the specified types
            if filename.lower().endswith(tuple(file_types)):
                # Build the full path to the image file
                filepath = os.path.join(MASTER_FOLDER, filename)

                # Open the image file and resize it
                img = cv2.imread(filepath)
                height, width = img.shape[:2]
                if height > width:
                    proportion = set_width / width
                    new_height = int(height * proportion)
                    new_width = set_width
                else:
                    proportion = set_height / height
                    new_width = int(width * proportion)
                    new_height = set_height
                img = cv2.resize(img, (new_width, new_height))

                # Crop the image to the desired size
                center = (new_width // 2, new_height // 2)
                crop_size = (set_width, set_height)
                img = cv2.getRectSubPix(img, crop_size, center)

                # Remove the background from the image
                if config.getboolean('background', 'remove_background'):
                    img = remove(img)

                # Blur the background from the image
                if config.getboolean('background', 'blur_background'):
                    # img = cv2.blur(img, (3, 3))
                    background = cv2.blur(img, (4, 4))
                    overlay = remove(img)
                    background_gray = cv2.cvtColor(background, cv2.COLOR_RGBA2RGB)
                    overlay_gray = cv2.cvtColor(overlay, cv2.COLOR_RGBA2RGB)
                    img = cv2.addWeighted(background_gray, 0.5, overlay_gray, 0.5, 0)

                # Normalize the pixel values of the image
                if config.getboolean('resolution', 'normalization'):
                    img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

                if config.getboolean('frame', 'rectangle_frame'):
                    bottom_layer = (255, 255, 255, 127)  # white color
                    img = cv2.rectangle(img, (0, 0), (set_width, set_height), bottom_layer, 10)  # add image frame

                # Black & white result.
                if config.getboolean('color', 'black_and_white'):
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

                # Rename the image file if necessary
                if not default_extension:
                    filename = os.path.splitext(filename)[0] + '.' + new_extension

                # Save the image file
                result_path = os.path.join(RESULT_FOLDER, filename)
                cv2.imwrite(result_path, img)

                # Print a message to indicate that the file has been processed
                print(f'{filename} has been resized and saved successfully!')

        print('Script is completed successfully!')

    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    image_resize()
