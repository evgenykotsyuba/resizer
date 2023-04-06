# import launch
import os
import configparser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REQ_FILE = os.path.join(CURRENT_DIR, "requirements.txt")
CONFIG_FILE = os.path.join(CURRENT_DIR, "config.ini")

config = configparser.ConfigParser()


# def install_missing_libraries():
#     with open(REQ_FILE) as file:
#         for lib in file:
#             lib = lib.strip()
#             if not launch.is_installed(lib):
#                 try:
#                     launch.run_pip(f"install {lib}", f"resizer/ requirement: {lib}")
#                 except Exception as e:
#                     print(f"Failed to install {lib}: {str(e)}")


def check_config_exist():
    if not os.path.isfile(CONFIG_FILE):
        config['location'] = {'master_model': 'master_model',
                              'result_model': 'result_model'}
        config['resolution'] = {'width': '512',
                                'height': '512',
                                'normalization': 'true'}
        config['type'] = {'file_type': 'jpg,jpeg,png,gif,webp',
                          'default_extension': 'false',
                          'new_extension': 'jpg'}
        config['background'] = {'remove_background': 'false'}
        config['color'] = {'black_and_white': 'false'}
        config['frame'] = {'rectangle_frame': 'false'}
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
        print(f'File config.ini created with default parameters at: {CONFIG_FILE}\n')
    else:
        try:
            config.read(CONFIG_FILE)
            if not config.sections():
                raise ValueError('Empty config file')
        except Exception as e:
            print(f"Error reading config file: {str(e)}")
            print(f"Please check the configuration file at: {CONFIG_FILE}\n")


if __name__ == '__main__':
    # install_missing_libraries()
    check_config_exist()
