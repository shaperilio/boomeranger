# Sorts images into sets based on capture time.

import os, shutil
from constants import *

set_offset = 0 # number for first set in this run.

files = os.listdir(input_dir)
if len(files) == 0:
    print('No files.')
    exit(0)

last_date = None
sets = []
for file in sorted(files):
    filename = os.path.join(input_dir, file)
    if os.path.isdir(filename):
        continue
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
    os.mkdir(new_dir)
    for old_file in set:
        # By putting a hyphen in the name, we can then use negative file numbers
        # to encode sequences in reverse.
        newFile = os.path.join(new_dir, f'image-{os.path.basename(old_file)[len(photo_prefix):]}')
        print(f'\t{old_file} --> {newFile}')
        shutil.move(old_file, newFile)