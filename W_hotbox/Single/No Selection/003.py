#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Save Frame
#
#----------------------------------------------------------------------------------------------------------

# diogo dubiella
# www.dubiella.com
# Save Frame 1.0

def saveFrame():
    viewer = nuke.activeViewer()
    inputNode = nuke.ViewerWindow.activeInput(viewer)
    viewNode = nuke.activeViewer().node()

    if inputNode != None:
        selInput = nuke.Node.input(viewNode, inputNode)
        filePath = nuke.getFilename('Save File', "*.png *.jpg *.tif *.exr", type = 'save')
        
        if filePath != None:
            
            filetype = filePath[-3:]
            filetypePonto = filePath[-4:]
            confirmfilr = filetypePonto[:1]
            
            if confirmfilr == ".":
                filetype = filePath[-3:]
                write = nuke.nodes.Write(file = filePath, name = 'WriteSaveThisFrame', file_type=filetype, raw=1)
                write.setInput(0,selInput)
                curFrame = int(nuke.knob("frame"))
                nuke.execute(write.name(), curFrame, curFrame)
                nuke.delete(write)
    else:
        nuke.message("This viewer don't have any input connected!")
saveFrame()