import cv2
import numpy as np

domain = " secret of mana sprite sheet"
orig = "..\downloads/"+domain+"/"
output = "../outputs/"+domain+"/"
img = "1.dd06dd6e55f71962a7dae2da86a0bb67.png"
file_name = "cascade"
extension = img[:-4]

# Count the most
def detectSimpleBackground(img):
    background_colour = 0
    return background_colour

# Sample image edges to quickly detect background colour
def detectSimpleBackgroundFast(img):
    background_colour = 0
    return background_colour

# Set all non-background objects to 1s, all background objects to 0s
def maskObjects(img, background_colour):
    masked_img = []
    return masked_img

# Using the masked image, detect the start and end point of each sprite by finding the min/max x/y
def floodFill(masked_img):
    minmaxes = []
    return minmaxes
    print("kay")

#1) detect background color (sample appropriately, say from image edges), one option is with votes in a hashtable (key = r+"-"+g+"-"+b)

#2) setup a mask, set all the background pixels to zero in mask within certain color distance of background, set all other mask pixels to 1.

#3) optionally: erode the mask once (or twice), then dilate back to remove useless lines.

#4) you now have a mask of 0 vs 1, do flood fill on each grouping of 1s to determine the extent of each sprite. Set mask pixels to "2" as you do the flood fill to indicate visited.

#5) as you flood fill, track each sprite's min/max x/y and at the end of the flood fill, you have the extents (and a mask) which can be used to crop/store.

