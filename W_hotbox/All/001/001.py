#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Branch
#
#----------------------------------------------------------------------------------------------------------

node = nuke.selectedNode()
 
# clean selection
for n in nuke.selectedNodes():
    n.setSelected(False)
 
# copy
node.setSelected(True)
nuke.nodeCopy("%clipboard%")
node.setSelected(False)
 
# paste
copyNode = nuke.nodePaste("%clipboard%")
copyNode.setSelected(False)
nuke.show(copyNode)
 
# connection
for i in range(node.inputs()):
    copyNode.setInput(i, node.input(i))
    
# positions
copyNode['xpos'].setValue(node.xpos()+55)
copyNode['ypos'].setValue(node.ypos()+55)