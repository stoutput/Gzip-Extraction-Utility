#!/bin/bash

# Script to extract all file*.gz files from specified folders
# USAGE: gz_unzip.sh 'directory 1' 'folder 2' 'folder/folder 3'
# Requires bash
# Written by: Benjamin Stout | 1/7/2016

# non-matching globs -> null
shopt -s nullglob

avg=0;
tests=4;

# run multiple iterations to calculate average runtime
for i in $(seq 1 $tests)
do
  startTime=$(date +%s%N)
  # iterate through each script parameter
  for folder in "$@"
  do
    if [ -d "$folder" ]
    then
      cd "$folder"
      # iterate over all gz files with file prefix in folder
      for gz in file*.gz
      do
        # make individual folder for extracted file
        filename="${gz%.*}"
        mkdir -p "$filename"
        # extract file from .gz archive to folder
        gunzip -cf "$gz" > "$filename"/"$filename"
        # zcat is slower
        #zcat -- "$gz" > "$filename"/"$filename" || true
        echo unzipped "$gz" to "$filename"
      done
      cd ..
    fi
  done

  # add runtime in ms to avg total
  avg=$((avg + (($(date +%s%N) - $startTime)/1000000)))

  #Delete all files and subfolders made by extraction
  for folder in "$@"
  do
    if [ -d "$folder" ]
    then
      cd "$folder"
      rm -R ./*/
      echo deleted extracted files in "$folder"
      cd ..
    fi
  done
done

# calculate average runtime for all iterations
avg=$((avg/tests))
echo Average runtime over "$tests" iterations equals "$avg" ms.
exit 0;
