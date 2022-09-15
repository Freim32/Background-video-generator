#Imports
import math
import utils


class Image:
    def __init__(self, position: tuple, size:int)-> None:
        self.original_image = None
        self.image = None
        self.image_name = None
        self.position = position
        self.size = size
        self_half_size = self.size / 2
        self.center = (self.position[0] + self_half_size / 2, self.position[1] + self_half_size / 2)
        self.half_diagonal = 0.75 * self.size
        
    def overlap(self, other_center:tuple, other_half_diagonal:int)->bool:
        "Check if Image overlay with a rectangle"
        distance = math.dist(self.center, other_center)
        return distance <= self.half_diagonal + other_half_diagonal 
    
    def set_png(self,name,image):
        "Set a png and resize it"
        self.original_image=image     
        self.image_name= name
        self.resize_image()
    
    def set_size(self,size):
        "Set new size and resize png"
        self.size=size
        self.resize_image()
    
    def resize_image(self):
        "Resize self.image"
        self.image = utils.resize_image(self.original_image,self.size,self.size)
        
    def change(self,step):
        "Change the size of the image and change the position to keep the center in the same spot"
        self.set_size(self.size+step)
        self.change_position(-step//2)
        
    def change_position(self,step):
        "Change the x and y by a given value"
        self.position=(self.position[0]+step,self.position[1]+step)
    
    def __repr__(self) -> str:
        "print image name, position and size"
        return f"{self.image_name} , {self.position} , {self.size}"
    
    def __str__(self) -> str:
        "print image name, position and size"
        return f"{self.image_name} , {self.position} , {self.size}"