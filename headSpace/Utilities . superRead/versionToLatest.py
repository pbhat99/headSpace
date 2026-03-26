#
# versionToLatest.py
#
# Cameron Carson [cameron.a.carson@gmail.com]
#
# Designed to replace the stock /"Version to Latest" function that will only update if the files are sequentially numbered.
# This Script will search the directory of your shot sequences and then look for ones with the same read name. It then substitutes the highest version it finds for the one in your read node.
#

import nukescripts
import nuke
import re
import os
import sys
from glob import glob

verbose = False

def versionToLatest():
    supported_reads = ["Read", "DeepRead", "ReadGeo"]
    for n in nuke.selectedNodes():
        currentnode = n
        classname = currentnode.Class()
        
        if classname in supported_reads:
            filename = nuke.filename(currentnode)
            if not filename:
                continue
                
            # Normalize path
            filename = filename.replace('\\', '/')
            splitDirs = filename.split("/")
            
            if len(splitDirs) < 2:
                continue
                
            fileDir = "/".join(splitDirs[:-2]) + "/"
            dirName = splitDirs[-2]
            dirPath = fileDir + dirName
            
            def sameName(path1, path2):
                if noVer(path1) == noVer(path2):
                    return True
                return False
            
            def pathVer(path):
                match = re.search(r'_[vV]\d+', path)
                if match:
                    return match.group(0)
                return None
            
            def noVer(path):
                splitPath = re.split(r'_[vV]\d+', path)
                if len(splitPath) >= 2:
                    return splitPath[0] + splitPath[1]
                return splitPath[0]
            
            current_ver = pathVer(filename)
            if not current_ver:
                if verbose:
                    print(f"No version pattern ('_v#') found in: {filename}")
                continue
            
            versionDict = {"seqs": []}
            if os.path.isdir(fileDir):
                for d in os.listdir(fileDir):
                    path = os.path.join(fileDir, d).replace('\\', '/')
                    if os.path.isdir(path):
                        if sameName(dirPath, path):
                            versionDict["seqs"].append(path)
            
            if not versionDict["seqs"]:
                continue
                
            maxVerPath = max(versionDict["seqs"])
            maxVer = pathVer(maxVerPath)
            
            if not maxVer or maxVer == current_ver:
                if verbose:
                    print(f"Already at latest version or no other versions found for: {currentnode.name()}")
                continue
                
            newFilename = filename.replace(current_ver, maxVer)
            currentnode['file'].setValue(newFilename)
            
            print(f"Node '{currentnode.name()}': version updated results in {maxVer}")
            
            newdirPath = dirPath.replace(current_ver, maxVer)
            
            def getFileSeq(dirPath):
                dirName_base = os.path.basename(dirPath)
                # COLLECT ALL FILES IN THE DIRECTORY THAT HAVE THE SAME NAME AS THE DIRECTORY (approximate sequence check)
                files = glob(os.path.join(dirPath, '*.*').replace('\\', '/'))
                files = [f for f in files if os.path.basename(f).startswith(dirName_base)]
                
                if not files:
                    return
                
                files.sort()
                
                try:
                    # GRAB THE RIGHT MOST DIGIT IN THE FIRST FRAME'S FILE NAME
                    firstString_matches = re.findall(r'\d+', os.path.basename(files[0]))
                    if not firstString_matches:
                        return
                    first = int(firstString_matches[-1])
                    
                    # GET LAST FRAME
                    lastString_matches = re.findall(r'\d+', os.path.basename(files[-1]))
                    if not lastString_matches:
                        return
                    last = int(lastString_matches[-1])
                    
                    # Update knobs if they exist (ReadGeo might lack origfirst/origlast)
                    if currentnode.knob('first'):
                        currentnode['first'].setValue(first)
                    if currentnode.knob('last'):
                        currentnode['last'].setValue(last)
                    if currentnode.knob('origfirst'):
                        currentnode['origfirst'].setValue(first)
                    if currentnode.knob('origlast'):
                        currentnode['origlast'].setValue(last)
                        
                except Exception as e:
                    if verbose:
                        print(f"Error updating frame range: {e}")
                return
            
            getFileSeq(newdirPath)
            
    return