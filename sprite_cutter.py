import cv2
import os
import numpy as np
import numpy as np

# Count the most
def detectSimpleBackground(img):
    colour = []
    for i in range(len(img)):
        for j in range(len(img[i])):
            colour.append(img[i][j])
    colours, counts = np.unique(colour, return_counts=True, axis=0)
    print(colours)
    top_id = 0
    top_count = 0
    for i in range(len(counts)):
        if counts[i] > top_count:
            top_count = counts[i]
            top_id = i



    print("bg colour is", colours[top_id])
    print("top left colour is", img[0][0])
    return colours[top_id]

# Sample image edges to quickly detect background colour
def detectSimpleBackgroundFast(img):
    background_colour = 0
    top_colours = []
    for i in range(len(img[0])):
        top_colours.append(img[0][i])

    bottom_colours = []
    for i in range(len(img[len(img)-1])):
        bottom_colours.append(img[len(img)-1][i])

    left_colours = []
    for i in range(len(img)):
        left_colours.append(img[i][0])

    right_colours = []
    for i in range(len(img)):
        right_colours.append(img[i][len(img[i])-1])
    all_colours = []

    all_colours.extend(top_colours)
    all_colours.extend(bottom_colours)
    all_colours.extend(left_colours)
    all_colours.extend(right_colours)

    all_colours, counts = np.unique(np.asarray(all_colours), return_counts = True, axis=0)

    top_count = 0
    top_id = 0
    for i in range(len(counts)):
        if counts[i] > top_count  :
            top_id = i
            top_count = counts[i]

    print("top colour is", all_colours[top_id])

    return all_colours[top_id]

# Set all non-background objects to 1s, all background objects to 0s
def maskObjects(img, background_colour):
    masked_img = np.empty(shape=(len(img), len(img[0])))
    for i in range(len(img)):
        for j in range(len(img[i])):
            if np.array_equal(img[i][j], background_colour):
                masked_img[i][j] = 0
                img[i][j] = [255,255,255]
            else:
                masked_img[i][j] = 1
    return masked_img, img

# Pure Python, usable speed but over 10x greater runtime than Cython version
def fill(data, start_coords, fill_value):
    """
    Flood fill algorithm

    Parameters
    ----------
    data : (M, N) ndarray of uint8 type
        Image with flood to be filled. Modified inplace.
    start_coords : tuple
        Length-2 tuple of ints defining (row, col) start coordinates.
    fill_value : int
        Value the flooded area will take after the fill.

    Returns
    -------
    None, ``data`` is modified inplace.
    """

    xsize, ysize = data.shape
    orig_value = data[start_coords[0], start_coords[1]]

    stack = set(((start_coords[0], start_coords[1]),))
    if fill_value == orig_value:
        raise ValueError("Filling region with same value "
                         "already present is unsupported. "
                         "Did you already fill this region?")
    top_x = 0
    top_y = 0
    bottom_x = 2147000000
    bottom_y = 2147000000
    while stack:
        x, y = stack.pop()
        # 5) as you flood fill, track each sprite's min/max x/y and at the end of the flood fill, you have the extents (and a mask) which can be used to crop/store.
        if x > top_x:
            top_x = x
        elif x < bottom_x:
            bottom_x = x
        if y > top_y:
            top_y = y
        elif y < bottom_y:
            bottom_y = y

        if data[x, y] == orig_value:


            data[x, y] = fill_value

            if x > 0:
                stack.add((x - 1, y))
            if x < (xsize - 1):
                stack.add((x + 1, y))
            if y > 0:
                stack.add((x, y - 1))
            if y < (ysize - 1):
                stack.add((x, y + 1))
    return data, [top_x, top_y, bottom_x, bottom_y]


def decomposeSpriteSheet(img):

    #1) detect background color (sample appropriately, say from image edges), one option is with votes in a hashtable (key = r+"-"+g+"-"+b)

    background_colour = detectSimpleBackgroundFast(img)

    if background_colour is None:
        print("Background colour was not consistent")
        return None

    #2) setup a mask, set all the background pixels to zero in mask within certain color distance of background, set all other mask pixels to 1.

    masked_img, bg_img = maskObjects(img, background_colour)

    print("masking done")

    all_coordinates = []
    for i in range(len(masked_img)):
        for j in range(len(masked_img[i])):
            if masked_img[i][j] == 1.0:
                new_img, coords = fill(masked_img, (i, j), 5)
                if (coords[0] - coords[2] > 10) and (coords[1] - coords[3] > 10):
                    all_coordinates.append(coords)

                break

    cropped_images = []
    for i in range(len(all_coordinates)):
        cropped_img = bg_img[all_coordinates[i][2]:all_coordinates[i][0], all_coordinates[i][3]:all_coordinates[i][1] ]
        cropped_images.append(cropped_img)
    return cropped_images

def getFns(folder_path):
    file_names = []
    onlyfiles = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for i in onlyfiles:
        file_names.append(i)
    return file_names, folder_path

def getFolders(folder_path):
    file_names = []
    onlyfiles = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) is False]
    for i in onlyfiles:
        file_names.append(i)
    return file_names, folder_path

orig = "data/sheets/"
output_orig = "data/sprites/"

fns, output_folder = getFolders("../sprite-sheet-downloader\cleaned")

for i in range(len(fns)):
    internal_fns, fn_output = getFns(output_folder + "/" + fns[i])
    for j in range(len(internal_fns)):
        print("data/sprites/"  + fns[i] + "/" + internal_fns[j] )
        img = cv2.imread(fn_output + "/" + internal_fns[j])

        if img is None:
            print("Image not found")
            exit()

        cropped_images = decomposeSpriteSheet(img)

        try:
            if os.path.exists("data/sprites/" + fns[i] ) is False:
                os.mkdir("data/sprites/" + fns[i] )
            if os.path.exists("data/sprites/"  + fns[i]+ "/" + internal_fns[j]) is False:
                os.mkdir("data/sprites/"  + fns[i] + "/" + internal_fns[j] )
        except FileExistsError:
            print("Folder exists")
        for k in range(len(cropped_images)):
            cv2.imwrite("data/sprites/"  + fns[i] + "/" + internal_fns[j] + "/" + str(k) + ".png", cropped_images[k])