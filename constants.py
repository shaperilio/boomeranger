# MP4 quality; lower is better
quality = 15

# Desired framerate
fps = 24

# Minimum number of sequential images that constitute a set. If less than this,
# images are assumed to be single still photos.
min_images_per_set = fps # one seconds' worth

# Minimum length of video; loop will be repeated until this is exceeded.
boomerang_length_seconds = 15

# Extension for a photo file (case sensitive)
photo_ext = '.JPG'

# Everything in the filename up to the image number, e.g. this is for photos
# named DSC05234.JPG
photo_prefix = 'DSC'

# Location of photos, e.g. where you copied the contents of your SD card. If
# your camera created multiple folders (e.g. the file counter has looped back to
# zero), point this to the folder containing the subfolders.
import os
input_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'DCIM')

# A regex pattern to search for a number in photo subdirectories; e.g. if
# `input_dir` contains subfolders '100MSDCF' and '101MSDCF', you want something
# that will extract the '100' and '101'. The first matching group is taken as
# the number.
subdir_number_pattern = '([0-9]+)'

# Location of the final boomerang videos
output_dir = os.path.join(input_dir, 'boomerangs')

# Desired video width. Images will be scaled to this. Must be even!
video_width = 1920

# Location of exiftool, as you'd type it into a terminal.
exiftool_call = 'exiftool'

# Location of ffmpeg
ffmpeg_call = 'ffmpeg'

if os.name == 'nt':
    dev_null = "NUL"
else:
    dev_null = '/dev/null'