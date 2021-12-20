# Sorts images into sets based on capture time.

import os, shutil
from constants import *
import re

set_offset = 0 # number for first set in this run.

files = os.listdir(input_dir)

# Check for directories or files.
has_files = False
has_directories = False
for file in sorted(files):
    filename = os.path.join(input_dir, file)
    if os.path.isdir(filename):
        has_directories = True
    elif os.path.isfile(filename):
        has_files = True

if not has_files and not has_directories:
    raise RuntimeError('No files or directories to sort through.')
if has_files and has_directories:
    raise RuntimeError('Found both files and directories. Cannot proceed.')

if has_directories:
    # Collect filenames from the subdirectories. We only go one deep.
    actual_files = []
    for d in sorted(files):
        dirname = os.path.join(input_dir, d)
        sub_files = os.listdir(dirname)
        for file in sorted(sub_files):
            actual_files.append(os.path.join(dirname, file))
else:
    actual_files = [os.path.join(input_dir, file) for file in sorted(files)]

last_date = None
sets = []
for filename in actual_files:
    if not photo_ext in filename:
        continue
    # mtime is the only one that works, sadly the resolution is not high enough
    # to detect when the camera buffer was full.
    this_date = os.path.getmtime(filename)
    if last_date is  None:
        this_set = [filename] # first time around; add file to set.
    else:
        time_delta_sec = this_date - last_date
        # Apparently within a burst, some files will have a time difference of 2
        # seconds.
        if time_delta_sec < 3:
            # Add file to this set; it was taken soon after the previous file.
            this_set.append(filename) 
        else:
            # Bigger jump in file date; assume this is the start of a new set.
            if len(this_set) >= min_images_per_set:
                # This sequence has enough images; make a set.
                print(f'Set with {len(this_set):3d} images formed; '
                      f'next file is {time_delta_sec:10.3f} seconds away')
                sets.append(this_set) # store the set
            else:
                # This sequence doesn't have enough images; ignore them.
                print(f'Set with {len(this_set):3d} images discarded (too short); '
                      f'next file is {time_delta_sec:10.3f} seconds away')

            this_set = [filename] # start a new set with this image.
    last_date = this_date

if len(this_set) >= min_images_per_set:
    # Trailing images got collected here. That's our last set.
    print(f'Set with {len(this_set):3d} images formed; arrived at last file.')
    sets.append(this_set)

# Now that the sets are formed, physically move the files into set folders.
for i in range(len(sets)):
    set = sets[i]
    set_num = i + set_offset
    print(f'set {set_num:2d}: {os.path.basename(set[0])} to {os.path.basename(set[-1])} '
          f'({len(set):3d} images)')

    new_dir = os.path.join(input_dir, 'set_%02d' % set_num)
    os.makedirs(new_dir, exist_ok=False)
    for old_file in set:
        # If we had subdirs, take digits from there to maintain image order
        # across folder boundaries.
        image_num_and_ext = os.path.basename(old_file)[len(photo_prefix):]
        if has_directories:
            subdir = os.path.basename(os.path.dirname(old_file))
            dir_num_match = re.search(subdir_number_pattern, subdir)
            if dir_num_match is None:
                raise RuntimeError(f'Photo subdirectory "{subdir}" has no numbers.')
            dir_num = dir_num_match[0]
            # By putting a hyphen in the name, we can then use negative file numbers
            # to encode sequences in reverse.
            # TODO: This doesn't work; it causes a large jump in the number and
            # ffmpeg won't follow the sequence. We need to remember the last
            # number and then add it to each subsequent dir, or do something
            # more clever.
            new_file = f'image-{dir_num}{image_num_and_ext}'
        else:
            new_file = f'image-{image_num_and_ext}'
        newFile = os.path.join(new_dir, new_file)
        print(f'\t{old_file} --> {newFile}')
        shutil.move(old_file, newFile)