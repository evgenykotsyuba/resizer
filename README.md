Project Name: Resizer
Image Resizer, Background Remover and Dataset Maker for Stable Diffusion

Description
This project is a Python script that resizes images in a folder and optionally removes their backgrounds using the rembg library. The configuration file specifies the location of the master and result folders, the resolution of the output images, the file types to process, and the file format for saving.

Installation
Clone the project repository from GitHub:

bash
Copy code
git clone https://github.com/evgenykotsyuba/resizer.git
Install the required Python libraries using pip:

Copy code
pip install -r requirements.txt
Usage
Place the images to be resized in the master folder specified in the configuration file.

Run the resize.py script:

python resize.py
The resized images will be saved in the result folder specified in the configuration file.

Configuration
The config.ini file specifies the following parameters:

location: the master and result folders where the input and output images are stored, respectively.
resolution: the width and height of the output images in pixels.
type: the file types to process and the file format for saving.
background: whether to remove the background from the images using the rembg library.
Credits
This project uses the rembg library for background removal, which can be found at https://github.com/danielgatis/rembg.

License
This project is licensed under the MIT License.