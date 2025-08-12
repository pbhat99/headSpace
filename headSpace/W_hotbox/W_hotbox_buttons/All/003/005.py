#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: copy bbox
#
#----------------------------------------------------------------------------------------------------------

def bboxMe():
    selected_node = nuke.selectedNode()
    sw = selected_node.screenWidth()
    sh = selected_node.screenHeight()
    print(sw)
    if not selected_node:
        return

    posX = selected_node.xpos()
    posY = selected_node.ypos()

    # Create Dot node before selected node
    before = nuke.createNode('Dot')

    before.setXpos(int(posX + sw / 2 - before.screenWidth() / 2))
    before.setYpos(int(posY + sh / 2 - before.screenHeight() / 2)- 50)

    # Create Dot node to the right of the first dot
    topRight = nuke.createNode('Dot')

    topRight.setXpos(int(posX + sw / 2 - before.screenWidth() / 2)+100)
    topRight.setYpos(int(posY + sh / 2 - before.screenHeight() / 2)- 50)

    # Create Dot node to the right of the bbox
    bottomRight = nuke.createNode('Dot')

    bottomRight.setXpos(int(posX + sw / 2 - before.screenWidth() / 2)+100)
    bottomRight.setYpos(int(posY + sh / 2 - before.screenHeight() / 2)+ 50)

    # Create Dot node after selected node
    bbox = nuke.createNode('CopyBBox')
    bbox.setXpos(posX)
    bbox.setYpos(int(posY + sh / 2 - before.screenHeight() / 2)+ 50)

    # Set connections
    before.setInput(0, selected_node.input(0))
    topRight.setInput(0, before)
    bottomRight.setInput(0, topRight)
    bbox.setInput(0, selected_node)
    bbox.setInput(1, bottomRight)

    # Connect selected Node
    selected_node.setInput(0, before)

bboxMe()