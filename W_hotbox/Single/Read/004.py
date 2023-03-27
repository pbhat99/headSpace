#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Convert to ReadGeo
#
#----------------------------------------------------------------------------------------------------------

nodeClass = 'ReadGeo'

selection = nuke.selectedNodes()

for node in selection:

  
    #save position
    position = [node.xpos(),node.ypos()]
    
    #save path
    fPath = node.knob('file').value()

    #make sure no nodes are selected
    for i in nuke.selectedNodes():
        i.knob('selected').setValue(False)

    #create new node
    newNode = nuke.createNode(nodeClass)
            
    newNode.knob('selected').setValue(False)


    #reconnect outputs
    node.knob('selected').setValue(True)
    tmpDotNode = nuke.createNode('Dot')
    node.knob('selected').setValue(False)
    
    tmpDotNode.setInput(0,newNode)
    nuke.delete(tmpDotNode)
        
    #delete original
    nuke.delete(node)
        
    newNode.setXpos(position[0])
    newNode.setYpos(position[1])
    newNode.knob('file').setValue(fPath)