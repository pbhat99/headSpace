import nuke
import os


############################################################################
#GET PATH SCRIPT
############################################################################
def getScriptPath():

    #'exr/nuke/script/script'   --> PREFIX
    #'exr/script/script'        --> NO PREFIX 
    
    #file EXR can be rendered with or without prefix
    metad_prefix = 'exr/nuke/script/script'
    metad_NOprefix = 'exr/script/script'
    
    found_metadata = False

    node = nuke.thisNode()
    
    
    
    #check if Read Node has metadata
    if node.metadata(metad_prefix) != None:
        filePath = node.metadata(metad_prefix)
        found_metadata = True
    elif node.metadata(metad_NOprefix) != None:
        filePath = node.metadata(metad_NOprefix)
        found_metadata = True
        
        
        
        
    #if metadata has been found    
    if (found_metadata == True):
        #check if file from metadata exists
        if os.path.isfile(filePath):
            ImportScript(filePath)
        else:
            #If file has not been found, ask to look for it
            if nuke.ask('Impossible to find the script in the original position: ' + filePath + '\nDo you want to look for the script?'):
                filePath = nuke.getFilename('Get a Nuke File', '*.nk *.gizmo')
                #If user select a file
                if filePath is not None:
                    ImportScript(filePath)
    else:
        #If file has not been found, ask to look for it
        if nuke.ask('File has no metadata.\nDo you want to look for the script?'):
            filePath = nuke.getFilename('Get a Nuke File', '*.nk *.gizmo')
            #If user select a file
            if filePath is not None:
                ImportScript(filePath)
        
        
############################################################################
#IMPORT SCRIPT BUTTON
############################################################################
def ImportScript(filePath):
        
            #GET FILE NAME
            fileName = (os.path.basename(filePath))
            
            #GET FILE SIZE
            #If size is bigger than 8MB, then give a message
            size = os.path.getsize(filePath)
            if size > 8000000:
                nuke.message("File is quite BIG and Importing could take some seconds. \nDon't close or move anything in Nuke")
            
            
            #CREATE GROUP
            group = nuke.createNode("Group")
            
            fileName = fileName.replace('.nk','')
            fileName = fileName.replace(' ','_')
    
            #CUSTOMIZE NODE GROUP
            group.knob('name').setValue("SCRIPT_IMPORTED_" + fileName)
            #group.knob('label').setValue(fileName + '\n' + filePath)
            group.knob('label').setValue(filePath)
            group.knob('note_font_size').setValue(20)
            group.knob('tile_color').setValue(0x99000000)
            group.knob('note_font_color').setValue(4294967041)
            group.knob('note_font').setValue("bold")
            #group.knob('note_font').setValue("italic")
            
            
            #PASTE INSIDE THE GROUP
            groupNode = nuke.toNode(group.name())
            groupNode.begin()
            
            nuke.nodePaste(filePath)
            
            groupNode.end()

############################################################################
#OPEN SCRIPT BUTTON
############################################################################
def OpenScript():

    #file EXR can be rendered with or without prefix
    metad_prefix = 'exr/nuke/script/script'
    metad_NOprefix = 'exr/script/script'
    
    found_metadata = False

    node = nuke.thisNode()
    
    
    
    #check if Read Node has metadata
    if node.metadata(metad_prefix) != None:
        filePath = node.metadata(metad_prefix)
        found_metadata = True
    elif node.metadata(metad_NOprefix) != None:
        filePath = node.metadata(metad_NOprefix)
        found_metadata = True
        
        
        
    #if metadata has been found    
    if (found_metadata == True):
        #check if file exists
        if os.path.isfile(filePath):
            nuke.scriptOpen(filePath)
        else:
            #If file has not been found, ask to look for it
            if nuke.ask('Impossible to find the script in the original position: ' + filePath + '\nDo you want to look for the file?'):
                filePath = nuke.getFilename('Get a Nuke File', '*.nk *.gizmo')
                #If user select a file
                if filePath is not None:
                    nuke.scriptOpen(filePath)
    else:
        nuke.message("File has no metadata")  