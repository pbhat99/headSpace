import os
import re
import nuke
import nukescripts

def superRead():
    """
    Main function for superRead tool
    Handles different scenarios based on selected nodes
    """
    selected_nodes = nuke.selectedNodes()
    
    if not selected_nodes:
        # No selection - run recursive load
        recursive_read()
    else:
        for p in selected_nodes:
            node_class = p.Class()

            # Check for write nodes
            if node_class in ['Write', 'WriteGeo', 'DeepWrite']:
                read_from_write_path(p)

            # Check for read nodes
            elif node_class in ['Read', 'ReadGeo', 'DeepRead', 'Camera']:
                update_to_latest_version(p)

            # Check other nodes with file knobs
            else:
                handle_file_knob_node(p)


def recursive_read():
    selected_path = nuke.getFilename("Please Select Root Folder")
    if not selected_path:
        return
    if os.path.isdir(selected_path):
        directory = selected_path
    else:
        nuke.message("Please select a directory")
        return
    file_paths = []
    results = os.walk(directory, followlinks=True)
    for dirpath, _, _ in results:
        filepaths = nuke.getFileNameList(dirpath)

        for filepath in filepaths:
            print (filepath)
            full_file_path = dirpath + '/' + filepath #os.path.join(dirpath, filepath) 
            if not os.path.isdir(full_file_path):
                file_paths.append(full_file_path)
                file_paths.sort() #edited

    for file_path_info in file_paths:
        try:
            # sequences
            results = file_path_info.split(" ")
            file_path, frame_range = results
            start_frame, end_frame = frame_range.split("-")
            nuke.nodes.Read(file=file_path, first=int(start_frame), last=int(end_frame))
        except ValueError:
            # single frame or video files
            read_node = nuke.createNode("Read")
            read_node.knob('file').fromUserText(file_path_info)
            

def read_from_write_path(write_node):
    try:
        file_path = write_node['file'].value()
        folder = os.path.dirname(file_path)
        video_extensions = ['.mov', '.mp4', '.avi']
        file_ext = os.path.splitext(file_path)[1].lower()
        project_start_frame = str(nuke.root()['first_frame'].value())

        if not file_path:
            nuke.message("Write node has no file path")
            return
        
        # Check for video file extensions
        
        # working needs code cleanup
        elif write_node.Class() == 'Write':
            if file_ext in video_extensions:
                read_node = nuke.createNode("Read")
                read_node.knob('file').fromUserText(file_path)
                read_node.knob('frame_mode').setValue('1')
                read_node.knob('frame').setValue(project_start_frame)
            else:
                for seq in nuke.getFileNameList(folder):
                    read_node = nuke.createNode('Read')
                    read_node.knob('file').fromUserText(folder + '/' + seq)

        elif write_node.Class() == 'WriteGeo':
            read_node = nuke.nodes.ReadGeo2(file=file_path)


        elif write_node.Class() == 'DeepWrite':
            for seq in nuke.getFileNameList(folder):
                read_node = nuke.createNode('DeepRead')
                read_node.knob('file').fromUserText(folder + '/' + seq)
        

        read_node.setXpos(write_node.xpos() + 100)
        read_node.setYpos(write_node.ypos() + 100)
        
        print ("Created read node from write path")
        
    except Exception as e:
        nuke.message("Error creating read from write: {}".format(str(e)))

def get_version_info(file_path):
    """
    Extract version information from file path
    Returns (base_path, version_number, extension)
    """
    # Common version patterns: v001, v01, _001, etc.
    version_patterns = [
        r'(_v|_V)(\d+)',  # v001, V001
        #r'(.+_)(\d+)(.+)',     # _001
        #r'(.+\.)(\d+)'   # .001.
    ]
    
    for pattern in version_patterns:
        match = re.match(pattern, file_path)
        if match:
            return match.groups()
    
    return None, None, None

def find_latest_version(file_path):
    """
    Find the latest version of a file
    Fixed to handle slashes properly and ensure proper path joining
    """
    base_path, current_version, extension = get_version_info(file_path)
    
    if not base_path:
        return file_path, 0  # No version found
    
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        return file_path, int(current_version) if current_version else 0
    
    # Look for all versions
    versions = []
    for filename in os.listdir(directory):
        # Properly join directory and filename with '/'
        full_path = directory + '/' + filename
        test_base, test_version, test_ext = get_version_info(full_path)
        
        if (test_base and test_ext and 
            os.path.basename(base_path) in os.path.basename(test_base) and
            test_ext == extension):
            try:
                versions.append((int(test_version), full_path))
            except ValueError:
                continue
    
    if versions:
        latest_version_num, latest_path = max(versions)
        return latest_path, latest_version_num
    
    return file_path, int(current_version) if current_version else 0

def update_to_latest_version(read_node):
    """
    Update read node to latest version or reload if already latest
    """
    try:
        file_path = read_node['file'].value()
        if not file_path:
            nuke.message("Read node has no file path")
            return
        
        latest_path, latest_version = find_latest_version(file_path)
        _, current_version, _ = get_version_info(file_path)
        
        current_ver_num = int(current_version) if current_version else 0
        
        if latest_path != file_path:
            # Update to latest version
            read_node['file'].setValue(latest_path)
            read_node['reload'].execute()
            print ("Updated to version {} (was version {})".format(latest_version, current_ver_num))
        else:
            # Already latest, just reload
            read_node['reload'].execute()
            print ("Already latest version ({}). Reloaded.".format(latest_version))
            
    except Exception as e:
        nuke.message("Error updating version: {}".format(str(e)))

def handle_file_knob_node(node):
    """
    Handle nodes with file knobs - either read from write path or update version
    """
    file_knobs = ['file', 'filename', 'path']
    file_knob = None
    
    # Find file knob
    for knob_name in file_knobs:
        if knob_name in node.knobs():
            file_knob = node[knob_name]
            break
    
    if not file_knob:
        nuke.message("Selected node has no file knob")
        return
    
    file_path = file_knob.value()
    if not file_path:
        nuke.message("File knob is empty")
        return
    
    # Check if this looks like a write path (ask user)
    result = nuke.ask("Update to latest version? (No = Create read from path)")
    
    if result:
        # Update version
        latest_path, latest_version = find_latest_version(file_path)
        _, current_version, _ = get_version_info(file_path)
        
        current_ver_num = int(current_version) if current_version else 0
        
        if latest_path != file_path:
            file_knob.setValue(latest_path)
            print ("Updated to version {} (was version {})".format(latest_version, current_ver_num))
        else:
            nuke.message("Already latest version ({})".format(latest_version))
    else:
        # Create read from path
        try:
            if file_path.lower().endswith(('.abc', '.obj', '.fbx')):
                read_node = nuke.nodes.ReadGeo2(file=file_path)
            else:
                read_node = nuke.nodes.Read(file=file_path)
            
            # Position near original node
            read_node.setXpos(node.xpos() + 200)
            read_node.setYpos(node.ypos())
            
            print ("Created read node from file path")
            
        except Exception as e:
            nuke.message("Error creating read: {}".format(str(e)))