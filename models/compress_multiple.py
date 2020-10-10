import sys
import os
import time
import argparse
import glob

from tfci import compress, decompress

# diable print
def disablePrint():
    sys.stdout = open(os.devnull, 'w')

# enable print
def enablePrint():
    sys.stdout = sys.__stdout__

def is_image(filename):
    return filename.split('.')[-1] == 'png' or filename.split('.')[-1] == 'jpg'
    #return filename.split('.')[-1] == 'jpg'

def start_compress(filename):
    lap_time = time.time()
    disablePrint()
    try:
        compress('hific-hi', filename, None)
    except:
        return 0, 0, 0, -1
    enablePrint()
    
    old_size = os.path.getsize(filename)
    new_size = os.path.getsize(filename + '.tfci')
    ratio = new_size/old_size
    return time.time()-lap_time, old_size, new_size, ratio

def process_files(args):
    dir_name = os.path.basename(os.path.normpath(args.image_dir))
    log = open('logs/log_compress_hi_{}_{:.0f}'.format(dir_name, time.time()), 'w')
    start_time = time.time()
    for dirpath, _, filenames in os.walk(args.image_dir):

        print('Compressing Folder {}'.format(dirpath))
        if args.num_images == 0:
            for f in filenames:
                
                if not is_image(f):
                    continue
                filename = os.path.join(dirpath, f)
                if os.path.isfile(filename + '.tfci'):
                    continue
                lap_time, old_size, new_size, ratio = start_compress(filename)
                log.write('{}, {}, {}, {:.4f} \n'.format(f, lap_time, old_size, new_size, ratio))
                #if os.path.isfile(filename + '.tfci'):
                #    decompress(filename + '.tfci', None)
        else:
            for i in range(min(args.num_images, len(filenames))):
                if not is_image(filenames[i]):
                    continue
                filename = os.path.join(dirpath, filenames[i])
                lap_time, old_size, new_size, ratio = start_compress(
                    filename)
                log.write('{} Lap Time: {:.2f} Original Size: {} Compressed Size: {} Ratio {:.4f} \n'.format(
                    filename, lap_time, old_size, new_size, ratio))

    #log.write('Total time compeleted: {:.2f}\n'.format(time.time() - start_time))
    log.close()


def main(**kwargs):
    description = "Compresses all image files in a directory"
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class= argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--image_dir", type=str, required=True, help="path to directory")
    parser.add_argument("-n", "--num_images", type=int, default=0, help="number of images to compress per folder")

    args = parser.parse_args()
    #input_images = glob.glob(os.path.join(args.image_dir, '*.jpg'))
    #input_images += glob.glob(os.path.join(args.image_dir, '*.png'))

    #assert len(
    #    input_images) > 0, 'No valid image files found in supplied directory!'

    process_files(args)
    
if __name__ == '__main__':
    main()
