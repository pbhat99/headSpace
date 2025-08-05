#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: premult
#
#----------------------------------------------------------------------------------------------------------

import nuke

def premultMe():
    selected_node = nuke.selectedNode()
    if not selected_node:
        return

    # Create Grade node before selected node
    before = nuke.createNode('Unpremult')
    before.setInput(0, selected_node.input(0))
    #before.setInput(1, selected_node)

    before.setXpos(selected_node.xpos())
    before.setYpos(selected_node.ypos() -50)


    # Create Grade node after selected node
    after = nuke.createNode('Premult')
    after.setInput(0, selected_node)
    after.setInput(1, None)

    after.setYpos(selected_node.xpos() +50)


    #connect selected Node
    selected_node.setInput(0,before)

premultMe()
