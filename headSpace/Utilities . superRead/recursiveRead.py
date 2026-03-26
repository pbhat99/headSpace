import os
import re
import nuke
import sys

# written by Howard Jones
# last modified 19-03-2026
# v1.0 - Updated for Python 3 and integrated by Antigravity

nameList = []
filesFound = []
ReadList = []
verbose = False
inStereo = True
# (source,replace) for all right to left conversions needed to match paths and filenames
stereoReplace = [('/right/', '/left/'), ('_right_', '_left_'), ('_right-', '_left-')]

def splitImgSeqs(path, files):
    if verbose:
        print(path)
    # Get a list of unique names in file
    for i in files:
        sp = i.split('.')
        name = sp[0]
        ext = sp[-1]
        name2CheckFor = str(name) + '.' + str(ext)
        if name2CheckFor not in nameList:
            nameList.append(name2CheckFor)
    
    for n in nameList:
        curList = []
        for i in files:
            p = path
            if not str(p).endswith('/'):
                p += '/'
            if verbose:
                print(p)

            if n.split('.')[0] in i:
                if n.split('.')[-1] in i:
                    curList.append(p + i)
        if curList:
            filesFound.append(curList)
        filesFound.sort()
    return filesFound

def imgSeq2NukeFormat(filesFound):
    for ff in filesFound:
        if not ff:
            continue
        
        first_file = ff[0]
        # Replace backslashes for consistency in Nuke
        first_file = first_file.replace('\\', '/')
        
        if verbose:
            print('Processing sequence starting with:', first_file)

        # Move on and ignore if the file is a hidden file
        if os.path.basename(first_file).startswith('.'):
            if verbose:
                print('Hidden file skipped:', first_file)
            continue

        # Split sequence into base, padding, and extension
        # We split from the right to avoid issues with dots in folder names
        parts = first_file.rsplit('.', 2)
        if len(parts) < 3:
            # Not a standard sequence format, add as single file
            ReadList.append(first_file)
            continue
            
        base, pad_example, ext = parts
        
        # Collect all frame numbers to find start and end
        frame_numbers = []
        for f in ff:
            f = f.replace('\\', '/')
            try:
                f_parts = f.rsplit('.', 2)
                if len(f_parts) == 3 and f_parts[1].isdigit():
                    frame_numbers.append(int(f_parts[1]))
            except (ValueError, IndexError):
                continue
        
        if not frame_numbers:
            # No valid frames found, treat as single file
            ReadList.append(first_file)
            continue
            
        start = min(frame_numbers)
        end = max(frame_numbers)
        
        # Determine padding from the first file in the group
        if pad_example.isdigit():
            padding = '#' * len(pad_example)
            # Nuke format: path/to/file.####.ext start-end
            readFile = "{}.{}.{} {}-{}".format(base, padding, ext, start, end)
        else:
            # Padding is not digits, likely not a sequence
            readFile = first_file
            
        ReadList.append(readFile)
    return ReadList

def stereoMatch(fileName):
    # replace right strings with left strings to match paths and files
    for src, repl in stereoReplace:
        pattern = re.compile(src)
        fileName = pattern.sub(repl, fileName)
    return fileName

def createReads(ReadList):
    for r in ReadList:
        if r.split(' ')[0][-3:] not in ('obj', 'fbx', 'abc'):
            if inStereo:
                if '/re/' in r:
                    r_left = stereoMatch(r)
                    rnleft = nuke.createNode('Read')
                    rnright = nuke.createNode('Read')
                    jv = nuke.createNode('JoinViews')
                    rnleft['file'].fromUserText(r_left)
                    rnright['file'].fromUserText(r)
                    jv.setInput(0, rnleft)
                    jv.setInput(1, rnright)
                elif '/le/' not in r:
                    rn = nuke.createNode('Read')
                    rn['file'].fromUserText(r)
            else:
                rn = nuke.createNode('Read')
                rn['file'].fromUserText(r)
        else:
            rn = nuke.createNode('ReadGeo')
            rn.setInput(0, None)
            rn['file'].fromUserText(r)

def getPath4Walk():
    directory = nuke.getClipname('Choose Folder', multiple=False)
    return directory

def recursive_read(v=False):
    """Entry point for superRead utility"""
    global verbose, nameList, filesFound, ReadList
    verbose = v
    # Clear global lists for sequential runs
    nameList = []
    filesFound = []
    ReadList = []
    
    walkPath = getPath4Walk()
    if not walkPath:
        return
        
    if verbose:
        print(walkPath)
    
    f = os.walk(walkPath)
    for i in f:
        splitImgSeqs(i[0], i[-1])
    
    if verbose:
        print('files found ', filesFound)
    
    readsList = imgSeq2NukeFormat(filesFound)
    
    if verbose:
        print(readsList)
    
    createReads(readsList)

def recursiveLoad(v=False):
    """Old entry point name kept for compatibility"""
    recursive_read(v)


 
 
