import os, shutil
from video_maker import fps

minImagesPerSet = fps # if less than this number of images makes a sequence, don't make it into a set.

dir = os.path.expanduser('~/Desktop/DCIM/100MSDCF')
setOffset = 0 # number for first set.
files = os.listdir(dir)
if len(files) == 0:
    print 'No files.'
    exit(0)

lastDate = None
sets = []
thisSet = []
for file in sorted(files):
    filename = os.path.join(dir, file)
    if os.path.isdir(filename): continue
    if not '.JPG' in filename: continue
    # mtime is the only one that works, sadly the resolution is not high enough to detect when the camera buffer was full.
    thisDate = os.path.getmtime(filename)
    if lastDate:
        timeDeltaSec = thisDate - lastDate
        if timeDeltaSec < 3: # Apparently within a burst, some files will have a time difference of 2 seconds.
            thisSet.append(filename) # add file to this set; it was taken soon after the previous file.
        else:
            # Bigger jump in file date; assume this is the start of a new set.
            if len(thisSet) >= minImagesPerSet:
                print 'Set with %3d images formed; next file is    %10.3f seconds away' % (len(thisSet), timeDeltaSec)
                sets.append(thisSet) # store the set
            else:
                print 'Set with %3d images discarded; next file is %10.3f seconds away' % (len(thisSet), timeDeltaSec)

            thisSet = [filename] # start a new one.
    else:
        thisSet.append(filename) # first time around; add file to set.
    lastDate = thisDate

if len(thisSet) >= minImagesPerSet:
    # Trailing images got collected here. That's our last set.
    print 'Set with %3d images formed; arrived at last file' % len(thisSet)
    sets.append(thisSet)

for i in range(0, len(sets)):
    set = sets[i]
    setNum = i + setOffset
    print 'set %2d: %s to %s (%3d images)' % (setNum, os.path.basename(set[0]),
                                             os.path.basename(set[-1]), len(set))

    newDirName = os.path.join(dir, 'set_%02d' % setNum)
    os.mkdir(newDirName)
    for oldFile in set:
        # By putting a hyphen in the name, we can then use negative file numbers to encode sequences in reverse.
        newFile = os.path.join(newDirName, 'image-%s' % os.path.basename(oldFile)[len('DSC'):])
        print '\t%s --> %s' % (oldFile, newFile)
        shutil.move(oldFile, newFile)