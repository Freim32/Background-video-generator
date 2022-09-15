#Import
import utils
import frame_generator

#SETTINGS

#Frames settings

#Path of background image
BACKGROUND_IMAGE_PATH = "Assets/Background/background.png"

#Path to the folder containing the images to add to the background
COMPONENT_IMAGE_FOLDER =  utils.get_project_path(1)+"/Assets/Image"

#Path where the individual frames will be saved
#The path must be complete otherwise ffmpeg goes crazy
FRAME_OUTPUT_FOLDER = utils.get_project_path(1)+"/Frame" 

#List of tuples containing the top right and bottom left vertices 
#of the drawable areas
DRAWABLE_AREAS_COORDINATES= [[[0,0],[425,233]],[[426,0],[851,233]],[[852,0],[1279,233]],[[0,232],[425,486]],[[852,232],[1279,486]],[[0,487],[425,719]],[[426,487],[851,719]],[[852,487],[1279,719]]]  

#Amount of pixels adjacent to the edge of the drawable 
# area where an image cannot be placed
DRAWABLE_AREAS_MARGIN = 40

#Maximum number of images for each drawable area
MAX_IMAGE_FOR_AREA = 2

#Minimum number of images for each drawable area
MIN_IMAGE_FOR_AREA = 1

#Possibility of failing to place an image
IMAGE_FAIL_PERCENTAGE = 50

#Minimum possible size for images
MIN_IMAGE_DIMENSION = 60

#Maximum possible size for images
MAX_IMAGE_DIMENSION = 120

#Animation settings

#Rate of change of each image compared to the previous frame
ANIMATION_STEP = 2   #If it is odd it could generate graphical bugs

#Minimum duration of each single animation
MIN_ANIMATION_DURATION = 2

#Maximum duration of each single animation
MAX_ANIMATION_DURATION = 6

#Video settings 

#Path where the created video will be saved
VIDEO_OUTPUT_FOLDER = "Output"

#Video name 
VIDEO_NAME = "Video01"

#Number of Frame per second of output video
FPS = 30

#Duration of the video in seconds
VIDEO_DURATION = 5 


@utils.timer()
def main():
    
    utils.remove_directory_all_files(
        FRAME_OUTPUT_FOLDER)
    
    frame_generator.generate_frames(
        DRAWABLE_AREAS_COORDINATES,
        DRAWABLE_AREAS_MARGIN,
        MAX_IMAGE_FOR_AREA,
        MIN_IMAGE_FOR_AREA,
        IMAGE_FAIL_PERCENTAGE,
        MIN_IMAGE_DIMENSION,
        MAX_IMAGE_DIMENSION,
        COMPONENT_IMAGE_FOLDER,
        BACKGROUND_IMAGE_PATH,
        VIDEO_DURATION,
        FPS,
        MIN_ANIMATION_DURATION,
        MAX_ANIMATION_DURATION,
        ANIMATION_STEP,
        FRAME_OUTPUT_FOLDER)

    utils.generate_video(
        FRAME_OUTPUT_FOLDER + '/%d.png',
        VIDEO_OUTPUT_FOLDER+ "/" + VIDEO_NAME + '.mp4',
        FPS)



if __name__ == "__main__":
    main()
    