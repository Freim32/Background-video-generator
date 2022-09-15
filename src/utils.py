#Imports
from ast import Global
from pyclbr import Function
from PIL import Image
import ffmpeg
import glob
import os 
import copy
import time

FUNCTION_COUNT = 0 

def timer(decimal=1):
    def decorator_function(f):
        def wrap(*args, **kwargs):
            time1 = time.monotonic()
            result = f(*args, **kwargs)
            time2 = time.monotonic()
            global FUNCTION_COUNT
            FUNCTION_COUNT+=1 
            print(f'{FUNCTION_COUNT}) '+'{:s} : {:.{}f} s'.format(f.__name__, ((time2-time1)*1), decimal ))
            return result
        return wrap
    return decorator_function

@timer()
def generate_video(images_path:str,output_path:str,framerate:int) ->None:
    "Generate a video starting from the images contained in the specified directory"
    (
        ffmpeg
            .input(images_path, framerate=framerate )
            .output(output_path,
                    preset="slow" ,
                    pix_fmt = "yuv420p",
                    level="3.0",
                    loglevel = "error",
                    **{'profile:v': "baseline"},
                    **{"c:v" :"libx264"},
                    **{"c:a" :"aac"})
            .run(overwrite_output=True)
    )
    return 

def remove_directory_all_files(folder:str) -> None:
    "Removes all files within the specified directory"
    files = glob.glob(folder+"/*")
    for file in files:
        os.remove(file)
    return

def get_project_path(remove_folder=0) -> str:
    """Gets the path of the folder where the file being executed is located,
    the "remove_folders" argument takes an integer and removes from the 
    returned path a number of folders from the end of the path equal to 
    the number indicated"""
    dirname = os.path.split(os.path.abspath(__file__))[0]
    
    if remove_folder: return "/".join([folder for folder in dirname.split("/")[0:-remove_folder]])
    
    return dirname

def resize_image(image: Image, new_width : int, new_height: int) -> Image:
    "It receives an image and returns one with the specified dimensions"
    new_image = copy.deepcopy(image)
    new_image.thumbnail((new_width, new_height), Image.ANTIALIAS)
    return new_image

def paste_image(upper_image:Image, lower_image:Image, position: tuple) -> Image:
    "Paste an image on top of a background image at a specific location"
    new_lower_image = copy.deepcopy(lower_image)
    new_lower_image.paste(upper_image, position, upper_image)
    return new_lower_image

def paste_images(upper_image_list:list,lower_image:Image) -> Image:
    "Paste a list of images on top of a background image in a specific position"
    new_lower_image = copy.deepcopy(lower_image)
    
    for area in upper_image_list:
        for upper_image in area:
             new_lower_image.paste(upper_image.image,upper_image.position,upper_image.image)
    
    return new_lower_image

