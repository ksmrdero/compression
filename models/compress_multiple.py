import sys, os
import time
path = os.path.dirname(os.path.abspath(__file__))

TEST_DIRECTORY = 'test2/'
arr = os.listdir(path + '/' + TEST_DIRECTORY)

# diable print
def disablePrint():
    sys.stdout = open(os.devnull, 'w')

# enable print
def enablePrint():
    sys.stdout = sys.__stdout__

log = open('log_compress_{:.0f}'.format(time.time()), 'w')
start_time = time.time()
for idx, filename in enumerate(arr):
    print('Compressing {}'.format(idx))
    if filename.split('.')[-1] == 'png' and 'tfci' not in filename:
        lap_time = time.time()
        disablePrint()
        os.system('python {}/tfci.py compress hific-lo {}'.format(path,
                                                                TEST_DIRECTORY + filename))
        enablePrint()
        old_size = os.path.getsize(TEST_DIRECTORY + filename)
        new_size = os.path.getsize(TEST_DIRECTORY + filename + '.tfci')

        log.write('{} File {} Lap Time: {:.2f} Total Time: {:.2f} Original Size: {} Compressed Size: {}\n'.format(
            filename, idx, time.time()-lap_time, time.time()-start_time, old_size, new_size))

log.write('Total time compeleted: {:.2f}\n'.format(time.time() - start_time))

log.close()
