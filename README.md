
# boomeranger
Python 3.x scripts that take sequences of images and makes "boomerang" style videos.

[constants.py](constants.py) - defines constants for both scripts.

[sorter.py](sorter.py) - takes photos from a folder and separates them into sets by looking
at capture time.

[video_maker.py](video_maker.py) - makes boomerang videos out of images in sets.

[togif.sh](togif.sh) and [togif_crop.sh](togif_crop.sh) - shell scripts to convert videos to animated
gifs.

## Dependencies
Requires [exiftool](https://sno.phy.queensu.ca/~phil/exiftool/) and [ffmpeg](http://ffmpeg.org/download.html)
