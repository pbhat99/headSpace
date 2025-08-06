#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: New Mask
#
#----------------------------------------------------------------------------------------------------------


def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()

emptySelection(selection)

for i in selection:

    rotoNode = nuke.createNode('Roto')
    postion = [i.xpos(),i.ypos()- round(i.screenHeight()/2)]
    rotoNode.setXpos(postion[0]+310)
    rotoNode.setYpos(postion[1])

    i.setInput(2,rotoNode)
    emptySelection(selection)