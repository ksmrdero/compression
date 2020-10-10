import sys
import os
import time
import argparse
import glob

from tfci import decompress

# diable print
def disablePrint():
    sys.stdout = open(os.devnull, 'w')

# enable print
def enablePrint():
    sys.stdout = sys.__stdout__

def process_files(args):
    log = open('logs/log_decompress_{:.0f}'.format(time.time()), 'w')
    start_time = time.time()
    for dirpath, _, filenames in os.walk(args.tfci_dir):
        for f in filenames:
            filename = os.path.join(dirpath, f)
            if filename.split('.')[-1] == 'tfci':
                if os.path.isfile(filename + '.png'):
                    continue
                lap_time = time.time()
                disablePrint()
                decompress(filename, None)
                enablePrint()
            
                log.write('{} Lap Time: {:.2f} Total Time: {:.2f}\n'.format(filename, time.time()-lap_time, time.time()-start_time))

    log.write('Total time compeleted: {:.2f}\n'.format(time.time() - start_time))
    log.close()

def main(**kwargs):
    description = "Decompresses all tfci files in a directory"
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class= argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--tfci_dir", type=str, required=True, help="path to directory")

    args = parser.parse_args()
    input_images = glob.glob(os.path.join(args.tfci_dir, '*.tfci'))

    assert len(
        input_images) > 0, 'No valid files found in supplied directory!'

    process_files(args)

if __name__ == "__main__":
    main()
