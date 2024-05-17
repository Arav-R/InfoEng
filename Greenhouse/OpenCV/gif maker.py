# Makes a gif based on images in a folder

import imageio
import os

files =  os.listdir(r'c:\Users\MakerSpaceAdmin\Documents\GitHub\InfoEng\Greenhouse\Photos') # folder path

image_path = [os.path.join(r'c:\Users\MakerSpaceAdmin\Documents\GitHub\InfoEng\Greenhouse\Photos', file) for file in files] # same path

images = []
for img in image_path:
    images.append(imageio.imread(img))

imageio.mimwrite(r'c:\Users\MakerSpaceAdmin\Documents\GitHub\InfoEng\Greenhouse\output.gif', images, fps= 2) # new generated gif path