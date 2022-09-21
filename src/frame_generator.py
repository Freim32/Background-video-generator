#Imports
import utils
import random
import image_class
import os 
import PIL

#Global variable
FRAME_NUMBER = 0  #It is used to give a sequential name to the generated frames 


def generate_frames(
    drawable_area_coordinates:list,
    drawable_area_margin:int,
    max_image_for_area:int,
    min_image_for_area:int,
    image_fail_percentage:int,
    min_image_dimension:int,
    max_image_dimension:int,
    component_image_folder:str,
    background_image_path:str,
    video_duration:int,
    FPS:int,
    min_animation_duration:int,
    max_animation_duration:int,
    animation_step:int,
    frame_output_folder:str) -> None:
    "Generate the individual frames needed to create the video"
    
    png_dict = load_assets(component_image_folder)
    
    drawable_areas = compute_drawable_areas(drawable_area_coordinates,drawable_area_margin)
    
    start_images = generate_starting_image(
        drawable_areas,
        max_image_for_area,
        min_image_for_area,
        image_fail_percentage,
        min_image_dimension,
        max_image_dimension,
        )
    
    add_png_to_Images(start_images,png_dict)
    
    video_background = PIL.Image.open(background_image_path)
    
    generate_animations(
        video_background,
        start_images,
        drawable_areas,
        video_duration,
        FPS,
        min_animation_duration,
        max_animation_duration,
        animation_step,
        frame_output_folder,
        min_image_dimension,
        max_image_dimension,
        png_dict)
    
    return 

def load_assets(component_image_folder:str):
    "Create a dictionary that contains the assets with their respective names"
    png_dict = {}
    for file in os.listdir(component_image_folder):
        png_dict[file] = PIL.Image.open(component_image_folder+"/"+file)
    return png_dict

def compute_drawable_areas(drawable_area_coordinates,drawable_area_margin) -> list:
    "It takes the coordinates of the drawable areas and modifies them in order to eliminate the indicated border"
    return [[[area[0][0]+drawable_area_margin,
              area[0][1]+drawable_area_margin],
             [area[1][0]-drawable_area_margin,
              area[1][1]-drawable_area_margin]]
            for area in drawable_area_coordinates]

@utils.timer()
def generate_starting_image(
    drawable_areas:list,
    max_image_for_area:int,
    min_image_for_area:int,
    image_fail_percentage:int,
    min_image_dimension:int,
    max_image_dimension:int,) -> list:
    
    "Generate the initial images with which the video will start"
    
    image_list=[]
    for area in drawable_areas:
        new_images = []    
        
        number_of_image = compute_number_of_images(max_image_for_area,min_image_for_area,image_fail_percentage)
        
        generate_images(area, number_of_image,min_image_dimension,max_image_dimension,new_images)
        
        image_list.append(new_images)
    
    return image_list

def compute_number_of_images(max_image_for_area:int,min_image_for_area:int,image_fail_percentage:int) -> int:
    "Calculate the number of images in a specific area"
    count = 0

    for _ in range(max_image_for_area):
        if image_fail_percentage <= random.randint(0,99): 
            count+=1
            
    return count if count > min_image_for_area else min_image_for_area 
    
def generate_images(area:list,n_images:int,min_image_dimension:int,max_image_dimension:int,new_images:list):
    """Recursive function that generates coordinated images and
    correspondents avoiding overlapping with existing images"""
    
    if n_images == len(new_images):
        return

    new_image = random_image(area, new_images, min_image_dimension,max_image_dimension)

    if new_image == None:
        new_images.pop()
    else:
        new_images.append(new_image)

    generate_images(area, n_images, min_image_dimension, max_image_dimension, new_images)   

def random_image(area:list,other_images:list,min_image_dimension:int,max_image_dimension:int) -> image_class.Image:
    "Create an image and its coordinates avoiding overlaps"
    
    size = random.randint(min_image_dimension//2,max_image_dimension//2) *2  # size is always even
    
    coordinates=random_coordinates(area,size,other_images)

    if coordinates:
        return image_class.Image(coordinates,size)
    
def random_coordinates(area,size,other_images) -> tuple:
    "Generate random coordinates until it finds valid ones"
    half_size=size // 2 
    
    n_loop = 0
    
    minX, maxX = area[0][0]+half_size,area[1][0]-half_size
    minY, maxY = area[0][1]+half_size,area[1][1]-half_size
    
    overlap = True
    
    while overlap :
        coordinates = (random.randint(minX,maxX),random.randint(minY,maxY))

        overlap = check_overlap(coordinates,size,other_images)
        
        #This magic number can improve the performance 
        #of the program if it is chosen well, tests have to be done 
        if n_loop == 500: return None       
        
        n_loop += 1
        
    return coordinates

def check_overlap(coordinates:tuple,size:int,other_images:list)-> bool:
    "Check for overlaps between a list of images"
    other_half_size = size / 2
    other_center = (coordinates[0] + other_half_size, coordinates[1] + other_half_size)
    other_half_diagonal = 0.75 * size
    
    for image in other_images:
        if image.overlap(other_center, other_half_diagonal):
            return True
    
    return False

@utils.timer()
def add_png_to_Images(start_images:list,png_dict:dict)-> None :
    "Adds png to Image objects, avoiding assigning the same png to two adjacent objects"
    png_set= set(png_dict.keys())
    
    for area in start_images:
        png_used= set()
        for image in area:
            if png_used != png_set:
                png_name = random.choice(tuple(png_set-png_used))
                png_used.add(png_name)
            else:
                png_name = random.choice(tuple(png_set))
            
            image.set_png(png_name,png_dict[png_name])

def add_png_to_Image(image:image_class.Image,png_used:set,png_dict:dict) -> None:
    "Adds png to Image object, avoiding assigning the same png to two adjacent objects"
    
    png_set= set(png_dict.keys())
    
    if png_used != png_set:
        png_name = random.choice(tuple(png_set-png_used))
    else:
        png_name = random.choice(tuple(png_set))
    
    image.set_png(png_name,png_dict[png_name])

@utils.timer()
def generate_animations(
    background:image_class.Image,
    start_images:list,
    drawable_areas:list,
    video_duration:int,
    FPS:int,
    min_animation_duration:int,
    max_animation_duration:int,
    animation_step:int,
    frame_output_folder:str,
    min_image_dimension:int,
    max_image_dimension:int,
    png_dict:dict) -> None:
    "Synchronize individual animations so that they are chained together"
    global FRAME_NUMBER
    
    video_duration = video_duration*FPS
    
    grow_image_area,drop_image_area = None,None
    
    while grow_image_area == drop_image_area:
        grow_image_area = random.randint(0,len(start_images)-1)
        drop_image_area = random.randint(0,len(start_images)-1)
        
    grow_image = start_images[grow_image_area].pop(0)
    drop_image = start_images[drop_image_area].pop(0)
        
    animation_bg = utils.paste_images(start_images,background)    
    
    while FRAME_NUMBER < video_duration:
        
        if (video_duration - FRAME_NUMBER) <= max_animation_duration * FPS:
            animation_duration = (video_duration - FRAME_NUMBER) // FPS
        else:
            animation_duration = random.randint(min_animation_duration,max_animation_duration)
        
        generate_animation(animation_bg,grow_image,drop_image,animation_duration,animation_step,FPS,frame_output_folder)
        
        start_images[grow_image_area].append(grow_image)
        
        old_areas = [grow_image_area,drop_image_area]

        grow_image_area = drop_image_area
        
        grow_image = None
        
        while not grow_image:
            grow_image = random_image(drawable_areas[grow_image_area],start_images[grow_image_area],min_image_dimension,max_image_dimension)
        
        add_png_to_Image(grow_image,{image.image_name for image in start_images[grow_image_area]},png_dict)
        
        while drop_image_area in old_areas:
            drop_image_area = random.randint(0,len(start_images)-1)
        
        drop_image = start_images[drop_image_area].pop(0)
        
        animation_bg = utils.paste_images(start_images,background)

    return

@utils.timer()
def generate_animation(
    background:image_class.Image,
    grow_image:image_class.Image,
    drop_image:image_class.Image,
    duration:int,
    animation_step:int,
    FPS:int,
    frame_output_folder:str)-> None:
    "Create individual animations"
    global FRAME_NUMBER
    
    empty_frame = compute_empty_frame(grow_image.size,drop_image.size,duration,animation_step,FPS)

    grow_image_size = grow_image.size
    grow_image.size=0
    
    frame = utils.paste_image(drop_image.image,background,drop_image.position)
    
    while grow_image.size < grow_image_size or drop_image.size > 0:

        for _ in range(empty_frame):
            frame.save(f"{frame_output_folder}/{FRAME_NUMBER}.png")
            FRAME_NUMBER+=1
        
        if grow_image.size + animation_step <= grow_image_size: 
            frame = image_animation(background,grow_image,animation_step)
        else:
            grow_image.set_size(grow_image_size)
            frame = utils.paste_image(grow_image.image,background,grow_image.position)
        
        if drop_image.size - animation_step > 0:
            frame = image_animation(frame,drop_image,-animation_step)
            
        else:
            drop_image.size = 0
        
  
        frame.save(f"{frame_output_folder}/{FRAME_NUMBER}.png")
        FRAME_NUMBER+=1
        
def compute_empty_frame(size1:int,size2:int,duration:int,animation_step:int,FPS:int) -> int:
    "Calculate how many frames in an animation must not have changes from the previous one"
    max_size= max(size1,size2)

    animation_frame = max_size // animation_step

    duration_frame =  duration * FPS

    duration_diff= duration_frame - animation_frame 

    empty_frame = duration_diff // animation_frame
    
    return empty_frame

def image_animation(background:image_class.Image,image:image_class.Image,step:int):
    "Edit individual images according to the animation"
    image.change(step)
    new_bg = utils.paste_image(image.image,background,image.position)
    return new_bg