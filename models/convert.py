import os
from PIL import Image

def convert(filename):
    im = Image.open(filename)
    # print(''.join(filename.split('.')[:-1])+'.png')
    im.save(''.join(filename.split('.')[:-1])+'.png')

files = list()
path = os.path.dirname(os.path.abspath(__file__))
for (dirpath, dirnames, filenames) in os.walk(path + '\\data\\seg_test'):
    files += [os.path.join(dirpath, file) for file in filenames]

for file in files:
    convert(file)
