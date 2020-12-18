from PIL import Image
import types
import sys
import glob
import os

CONST_EXTENSION = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
CONST_SIGN = "_razor_images"
CONST_ALIGN = 4
CONST_OFFSET = 5

def greyscale(color):
    if (type(color) == tuple):
        res = (color[0] + color[1] + color[2]) / 3
    else:
        res = color
    return res

def limit(image, cropGrey):
    """
    crop an image based on the size limit
    image: an image object in RGB
    cropGrey: expected size
    """
    xsize, ysize = image.size
    print(xsize, ysize)
    # print(image.getpixel((xsize-1, ysize-1)))
    crop = [None, None, None, None]
    for y in range(ysize):
        for x in range(xsize):
            grey = greyscale(image.getpixel((x,y)))
            if grey > cropGrey:
                crop[1] = y
                break
        if crop[1] != None:
            break
    for y in range(ysize-1, -1, -1):
        for x in range(xsize):
            grey = greyscale(image.getpixel((x,y)))
            if grey > cropGrey:
                crop[3] = y
                break
        if crop[3] != None:
            break
    for x in range(xsize):
        for y in range(ysize):
            grey = greyscale(image.getpixel((x,y)))
            if grey > cropGrey:
                crop[0] = x
                break
        if crop[0] != None:
            break
    for x in range(xsize-1, -1, -1):
        for y in range(ysize):
            grey = greyscale(image.getpixel((x,y)))
            if grey > cropGrey:
                crop[2] = x
                break
        if crop[2] != None:
            break
    return crop

def get_files(files, actDir):
    os.chdir (actDir)
    dirs = []
    elements = glob.glob ("*")

    for x in range (len (elements)):
        if (os.path.isdir (elements[x])):
            dirs.append (elements[x])

    for x in range (len (CONST_EXTENSION)):
        type = glob.glob ("*" + CONST_EXTENSION[x])
        # pridani absolutni cesty
        for x in range (len (type)):
            type[x] = os.path.join (actDir, type[x])
        files += type

    if (dirs != []):
        for x in range (len (dirs)):
            get_files (files, os.path.join (actDir, dirs[x]))
    return files

def make_dirs(actDir, input, output):
    os.chdir (actDir)
    dirs = []
    elements = glob.glob ("*")
    outDir = str.replace(actDir, input, output)

    for x in range (len (elements)):
        if (os.path.isdir (elements[x])):
            new = os.path.join (outDir, elements[x])
            act = os.path.join (actDir, elements[x])
            if (os.path.isdir (new) == False):
                os.mkdir (new)
            dirs.append (act)

    if (dirs != []):
        for x in range (len (dirs)):
            make_dirs (dirs[x], input, output)

def print_stats(file, sizeImg, sizeReg):
    spaceImg = []
    spaceReg = []
    spaceImg.append (CONST_ALIGN - len (str (sizeImg[0])))
    spaceImg.append (CONST_ALIGN - len (str (sizeImg[1])))
    spaceReg.append (CONST_ALIGN - len (str (sizeReg[0])))
    spaceReg.append (CONST_ALIGN - len (str (sizeReg[1])))
    strImg = spaceImg[0] * " " + str (sizeImg[0]) + " x " + spaceImg[1] * " " + str (sizeImg[1])
    strReg = spaceReg[0] * " " + str (sizeReg[0]) + " x " + spaceReg[1] * " " + str (sizeReg[1])
    print(strImg + CONST_OFFSET * " " + strReg + CONST_OFFSET * " " + file)

# error messages
def ErrorArg():
    print("ERROR: Incorrect arguments!\nTo show help, run program with parameter -h.")
    return

def ErrorDir(dir):
    print("ERROR: Directory " + dir + " doesn't exist!")
    return

def ErrorOpen(file):
    print("ERROR: Cannot open image file: " + file)
    return

def ErrorSave(file):
    print("ERROR: Cannot save image file: " + file)
    return

def edge_detection(inputpath):
    """
    detect and remove black edges of an image
    inputpath: the path to an image
    """
    crop_grey = 160
    # tolerance = 200
    output = inputpath.split('.')[0] + '_edge_removed.jpg'
    image = Image.open(inputpath)
    imageRgb = image.convert("RGB")
    crop = limit(imageRgb, crop_grey)
    # save = str.replace (files[i], inputpath, output)
    region = image.crop((crop[0], crop[1], crop[2], crop[3]))
    region.load()
    region.save(output)
    return output
