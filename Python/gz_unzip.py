# Script to extract all file*.gz files from specified folders
# USAGE: gz_unzip.py 'directory 1' 'folder 2' 'folder/folder 3'
# Requires Python > 2.7
# Written by: Benjamin Stout | 1/7/2016
import sys
import os
import glob
from multiprocessing import Pool
import subprocess
import shutil
import errno
import datetime as dt

# Function to provide similar functionality to the mkdir -p command
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# Function to extract contents of .gz file into individual folder of same name
def extract_gz(path):
    # make directory for extracted file
    mkdir_p(path)
	# open/create destination file
    dest = open(path+'/'+os.path.basename(path), 'wb')
    # copy contents of .gz file using a zcat subprocess
    src = subprocess.Popen(['zcat',path+'.gz'], stdout=dest)
    dest.close()

    # ---- Using the gzip library is slower than zcat...
    # with BufferedReader(gzip.open(filepath, 'rb')) as src, open(destpath, 'wb') as dest:
	# 	# copy data from src to dest in 100kb blocks
    #     for block in iter(lambda: src.read(100000),""):
    #         dest.write(block)
    print "Extracted ",path

# Function to facilitate extraction
def main(argv):
    # get current working directory
    cwd = os.getcwd()
    # runtime testing flag - preserves or deletes extracted files
    test = True
    # number of iterations to average runtime over
    iterations = 4
    # average runtime counter
    avg = 0

    for i in range(iterations):
        # start timer
        start = dt.datetime.now()
        # array of all filenames
        filenames = []
        # iterate through each folder passed as script arg
        for path in argv:
            folder = cwd+'/'+path
            if (os.path.isdir(folder)):
                for gz in glob.glob(folder+"/file*.gz"):
                    # add all file*.gz paths to filenames array
                    filenames.append(gz[:-3]) # slice .gz extension

        # start multiprocessing pool to extract files
        pool = Pool()
        # pass extractions to pool in chunks of number of files/4*number of workers in pool
        for _ in pool.imap_unordered(extract_gz, filenames, chunksize=len(filenames)/(4*pool._processes)):
            pass

        # add runtime in ms to average counter
        runtime = dt.datetime.now() - start
        avg += int(runtime.total_seconds() * 1000)

        # delete extracted files
        if test or i == iterations-1:
            for path in filenames:
                shutil.rmtree(path)
                print "Deleted ",path

    avg /= iterations # divide total by # of iterations
    print "Average runtime over ",iterations," iterations equals ",avg,"ms"

if __name__ == "__main__":
    # pass all but first script arguments to main()
    main(sys.argv[1:])
