###   Adds a Reader from selected Write node(s)
###   v3.1 - Last modified: 19-03-2026
###   Written by Diogo Girondi modified by prasanna
###   diogogirondi@gmail.com

import os
import stat
import nuke
from time import strftime

def readwrites(blankread=True, check=True, threshold=100000, report=True):
    
    """
    Spawns a Read node(s) from selected Write node(s) and check it's files.
    
    readwrites(arg1, arg2, arg3)
    
    arg1: True: Spawn blank read with empty selections or write nodes
             False: Don't spawn anything for empty selections or write nodes
            
    arg2: True or False, Check for suspicious file sizes in the source folder.
    
    arg3: Integer, set's the threshold for bad files in bytes
    
    arg4: True or False, prints a report of the suspecious files to the terminal
    
    """
    
    def _checkbadframes(node, report):
        
        file = node.knob('file').value()
        folder = file.rstrip(file.split('/').pop())
        
        suspects = {}
            
        for f in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, f)):
                file_size = os.stat(os.path.join(folder, f)).st_size
                if file_size < threshold:
                    suspects[f] = int(file_size)
                    
        if suspects != {}:
            node.knob('tile_color').setValue(-1308622593)
            
            if report == True:
                
                ordered_suspects = sorted(suspects.items(), key=lambda x: (x[0], x[1]))
                tprintlist = []
                spacing = 14
                GB = 1073741824.0
                MB = 1048576.0
                KB = 1024.0
                
                for each in ordered_suspects:
                    if each[1] < KB:
                        size = f"{each[1]} bytes"
                    elif each[1] < MB:
                        size = f"{each[1] / KB:.1f} KB"
                    elif each[1] < GB:
                        size = f"{each[1] / MB:.2f} MB"
                    else:
                        size = f"{each[1] / GB:.0f} GB"
                        
                    tprintlist.append(f"- {each[0]}  {size}")
                
                for each in tprintlist:
                    if len(each) > spacing:
                        spacing = len(each)
                
                div = "=" * spacing
                header = f"__File{'_' * (spacing - 13)}Size___"
                
                nuke.tprint("")
                nuke.tprint(div)
                nuke.tprint(f'{strftime("%H:%M:%S")} Bad frames for: {node.name()}')
                nuke.tprint(div)
                nuke.tprint(header)
                for each in tprintlist:
                    nuke.tprint(each)
                nuke.tprint(div)
                
            else:
                pass
                
        return None
    
    
    def _readwrites(blankread, check, threshold, report):
        
        # Filter for all common Write node types
        supported_writes = ["Write", "WriteGeo", "DeepWrite"]
        sn = [n for n in nuke.selectedNodes() if n.Class() in supported_writes]
        
        if not sn and blankread:
            nuke.createNode("Read", "", True)
            return None
            
        elif not sn and not blankread:
            return None
            
        for n in sn:
            node_class = n.Class()
            xpos = n.knob('xpos').value()
            ypos = n.knob('ypos').value()
            
            # Basic info common to all
            file_path = n.knob('file').value() if n.knob('file') else ""
            proxy_path = n.knob('proxy').value() if n.knob('proxy') else ""
            
            # Frame range (might be missing in some node types or manual)
            first_frame = nuke.value(f"{n.name()}.first_frame", "")
            last_frame = nuke.value(f"{n.name()}.last_frame", "")
            
            # Read node type mapping
            read_class = "Read"
            if node_class == "DeepWrite":
                read_class = "DeepRead"
            elif node_class == "WriteGeo":
                read_class = "ReadGeo"
            
            if not file_path and not proxy_path:
                if blankread:
                    read = nuke.createNode(read_class, "", False)
                    read.setXYpos(int(xpos), int(ypos + 80))
                    nuke.inputs(read, 0)
                continue
            
            # Collection of optional knobs
            knobs_to_copy = {
                'colorspace': 'colorspace',
                'premultiplied': 'premultiplied',
                'raw': 'raw'
            }
            
            # Create the node
            read = nuke.createNode(read_class, "", False)
            read.setXYpos(int(xpos), int(ypos + 80))
            nuke.inputs(read, 0)
            
            # Set knobs manually for better compatibility across types
            if file_path:
                read.knob('file').setValue(file_path)
            if proxy_path and read.knob('proxy'):
                read.knob('proxy').setValue(proxy_path)
            if first_frame and read.knob('first'):
                read.knob('first').setValue(int(float(first_frame)))
            if last_frame and read.knob('last'):
                read.knob('last').setValue(int(float(last_frame)))
                
            for w_knob, r_knob in knobs_to_copy.items():
                if n.knob(w_knob) and read.knob(r_knob):
                    read.knob(r_knob).setValue(n.knob(w_knob).value())
            
            if check:
                _checkbadframes(read, report)
                
        return None
    
    _readwrites(blankread, check, threshold, report)
    
