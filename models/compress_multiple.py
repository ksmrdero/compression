import sys
import os
import argparse
import glob

from tfci import compress, decompress

def is_image(filename):
    return filename.split('.')[-1] == 'png' or filename.split('.')[-1] == 'jpg'


def start_compress(model, filename, output_path):
    try:
        compress(model, filename, output_path)
    except:
        return False
    return True


def process_files(args):
    dir_name = os.path.basename(os.path.normpath(args.image_dir))
    parent_path = os.path.dirname(args.image_dir)
    log = open('logs/log_compress_{}_{}'.format(args.model, dir_name), 'w')

    # tfci path
    
    tfci_folder_path = os.path.join(parent_path, '{}_{}_tfci'.format(dir_name, args.model))
    if not os.path.exists(tfci_folder_path):
        os.mkdir(tfci_folder_path)

    filenames = os.listdir(args.image_dir)
    for filename in filenames:
        if not is_image(filename):
            continue

        file_path = os.path.join(args.image_dir, filename)
        if os.path.isfile(filename + '.tfci'):
            continue
        
        tfci_path = os.path.join(tfci_folder_path, filename + '.tfci')
        if not start_compress(args.model, file_path, tfci_path):
            continue

        old_size = os.path.getsize(file_path)
        new_size = os.path.getsize(tfci_path)
        ratio = new_size/old_size

        log.write('{}, {}, {}, {:.4f} \n'.format(
            filename, old_size, new_size, ratio))

    log.close()


def main(**kwargs):
    description = "Compresses all image files in a directory"
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--image_dir", type=str,
                        required=True, help="path to directory")
    parser.add_argument("-m", "--model", type=str,
                        required=True, help="compression model")

    args = parser.parse_args()
    input_images = glob.glob(os.path.join(args.image_dir, '*.jpg'))
    input_images += glob.glob(os.path.join(args.image_dir, '*.png'))

    assert len(
       input_images) > 0, 'No valid image files found in supplied directory!'

    process_files(args)


if __name__ == '__main__':
    main()
