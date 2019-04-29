import os, glob, math

dir = os.path.expanduser('~/Desktop/100MSDCF')

quality = 15 # MP4 quality; lower is better
fps = 24
boomerangLengthSeconds = 15 # final video length, minimum.
sets = sorted(glob.glob('%s/set_*' % dir))
for set in sets:
    if not os.path.isdir(set): continue
    files = sorted(glob.glob('%s/*.JPG' % set))
    setName = os.path.basename(set)
    print setName
    # Start at the second frame, because the reverse clip will end at the first frame.
    startNum = int(os.path.basename(files[1])[len('image-'):-len('.JPG')])
    videoFileForward = os.path.join(dir, '%s_forward.mp4' % setName)
    ffmpeg = "ffmpeg -y -start_number %d -r %d -i '%s/image-%%05d.JPG' -vf scale=1920:1280 -vcodec libx264 " \
             "-crf %d -pix_fmt yuv420p %s" % (startNum, fps, set, quality, videoFileForward)
    print 'Forward'
    os.system(ffmpeg)

    # Reverse clip starts at the second to last frame, because the forward clip ends at the last frame.
    startNum = int(os.path.basename(files[-2])[len('image'):-len('.JPG')])
    videoFileReverse = os.path.join(dir, '%s_reverse.mp4' % setName)
    ffmpeg = "ffmpeg -y -start_number %d -r %d -i '%s/image%%05d.JPG' -vf scale=1920:1280 -vcodec libx264 " \
             "-crf %d -pix_fmt yuv420p %s" % (startNum, fps, set, quality, videoFileReverse)
    print 'Reverse'
    os.system(ffmpeg)

    # How long is our sequence?
    numFrames = len(files)
    lengthSeconds = numFrames / float(fps) * 2 # 2 for forward and reverse
    numPairs = int(math.ceil(boomerangLengthSeconds / lengthSeconds))

    print 'Pair is %.2f seconds long. Will require %d pairs to hit %d seconds.' % (
        lengthSeconds, numPairs, boomerangLengthSeconds
    )
    # Make the concat list.
    with open('/tmp/concat.txt', 'w') as f:
        for i in range(0, numPairs):
            f.write('file %s\n' % videoFileForward)
            f.write('file %s\n' % videoFileReverse)

    videoFile = os.path.join(dir, '%s_boomerang.mp4' % setName)

    ffmpeg = "ffmpeg -y -safe 0 -f concat -i '/tmp/concat.txt' -c copy %s" % (videoFile)
    print 'Concat'
    print ffmpeg
    os.system(ffmpeg)
