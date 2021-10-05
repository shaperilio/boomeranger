# Make videos from images that have been sorted into sets.

import os, glob, math, tempfile
from constants import *

temp_dir = tempfile.mkdtemp(prefix='video_maker_')

def get_output(cmd: str) -> str:
    # Super lazy way to get the output of a program: output to a file and then
    # read that file.
    temp_file = os.path.join(temp_dir, 'temp.txt')
    os.system(f'{cmd} > {temp_file}')
    with open(temp_file, 'r') as f:
        return f.read()

sets = sorted(glob.glob(f'{input_dir}/set_*'))
output_dims = None
for set in sets:
    if not os.path.isdir(set): continue
    files = sorted(glob.glob(f'{set}/*{photo_ext}'))
    if len(files) < min_images_per_set:
        print('Set does not contain enough images!')
        continue
    set_name = os.path.basename(set)
    print(set_name)
    if output_dims is None:
        # We have to compute our own output size, maintaining aspect ratio, and
        # making sure the height is divisible by 2.
        exiftool = f'{exiftool_call} -ImageWidth -s -s -s {files[0]}'  # -s 3 times gets value only
        width = int(get_output(exiftool))
        exiftool = f'{exiftool_call} -ImageHeight -s -s -s {files[0]}'  # -s 3 times gets value only
        height = int(get_output(exiftool))
        AR = height / float(width)
        new_width = video_width
        new_height = int(new_width * AR)
        if new_height % 2:
            new_height -=1
        output_dims = f'{new_width}x{new_height}'
        print(f'{width}x{height} -> {output_dims}')
    # Check the orientation of these images. Currently only support "horizontal"
    # and "90 CW".
    exiftool = f'{exiftool_call} -Orientation -n {files[0]}'
    orientation = get_output(exiftool)
    if ': 1' in orientation:
        vf = f'scale={output_dims}'
        print('Images are horizontal')
    elif ': 6' in orientation:
        vf = f'scale={output_dims},transpose=1' # see https://stackoverflow.com/a/9570992
        print('Images are vertical')
    else:
        raise RuntimeError(f'Unsupported image rotation!\n{orientation}')
    # Start at the second frame, because the reverse clip will end at the first frame.
    start_num = int(os.path.basename(files[1])[len('image-'):-len(photo_ext)])
    vid_file_fwd = os.path.join(input_dir, f'{set_name}_forward.mp4')
    ffmpeg = f"{ffmpeg_call} -y -start_number {start_num} -r {fps} -i \"{set}/image-%05d.JPG\" " \
             f"-vf \"{vf}\" -vcodec libx264 -crf {quality} -pix_fmt yuv420p {vid_file_fwd} " \
             f"> {dev_null} 2>&1"
    print('Forward')
    os.system(ffmpeg)

    # Reverse clip starts at the second to last frame, because the forward clip ends at the last frame.
    start_num = int(os.path.basename(files[-2])[len('image'):-len(photo_ext)])
    vid_file_rev = os.path.join(input_dir, f'{set_name}_reverse.mp4')
    ffmpeg = f"{ffmpeg_call} -y -start_number {start_num} -r {fps} -i \"{set}/image%05d.JPG\" " \
             f"-vf \"{vf}\" -vcodec libx264 -crf {quality} -pix_fmt yuv420p {vid_file_rev} " \
             f"> {dev_null} 2>&1"
    print('Reverse')
    os.system(ffmpeg)

    # How long is our sequence?
    num_frames = len(files)
    len_seconds = num_frames / float(fps) * 2 # 2 for forward and reverse
    num_pairs = int(math.ceil(boomerang_length_seconds / len_seconds))

    print(f'Pair is {len_seconds:.2f} seconds long. Will require {num_pairs} pairs to hit '
          f'{boomerang_length_seconds} seconds.')

    # Make the concat list.
    concat_file = os.path.join(temp_dir, 'concat.txt')
    # ffmpeg needs the backslashes escaped when loading a file list from a file.
    fwd = vid_file_fwd.replace("\\", "\\\\")
    rev = vid_file_rev.replace("\\", "\\\\")
    with open(concat_file, 'w') as f:
        for i in range(num_pairs):
            f.write(f'file {fwd}\n')
            f.write(f'file {rev}\n')

    video_file = os.path.join(output_dir, f'{set_name}_boomerang.mp4')

    ffmpeg = f"{ffmpeg_call} -y -safe 0 -f concat -i \"{concat_file}\" -c copy {video_file} > {dev_null} 2>&1"
    print('Concat')
    os.system(ffmpeg)
    print()