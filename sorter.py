import os, shutil

dir = os.path.expanduser('~/Desktop/100MSDCF')
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
            print 'Start of set: %s - %10.3f' % (file, timeDeltaSec)
            sets.append(thisSet) # store the set
            thisSet = [filename] # start a new one.
    else:
        thisSet.append(filename) # first time around; add file to set.
    lastDate = thisDate

if len(thisSet) > 0:
    # Trailing images got collected here. That's our last set.
    sets.append(thisSet)

for i in range(0, len(sets)):
    set = sets[i]
    setNum = i + setOffset
    print 'set %2d: %s to %s (%3d images)' % (setNum, os.path.basename(set[0]),
                                             os.path.basename(set[-1]), len(set))
    if len(set) < 2:
        print 'Not enough images to make a set!'
        continue

    newDirName = os.path.join(dir, 'set_%02d' % setNum)
    os.mkdir(newDirName)
    for oldFile in set:
        # By putting a hyphen in the name, we can then use negative file numbers to encode sequences in reverse.
        newFile = os.path.join(newDirName, 'image-%s' % os.path.basename(oldFile)[len('DSC'):])
        print '\t%s --> %s' % (oldFile, newFile)
        shutil.move(oldFile, newFile)