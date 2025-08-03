#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: reFormat
#
#----------------------------------------------------------------------------------------------------------

sn = nuke.selectedNode()
if sn:
    for i in range(sn.inputs()):
        if sn.input(i):
            before = nuke.nodes.Reformat(type = 2, resize = 0, xpos = sn.xpos()+ (-100*i), ypos = sn.ypos() - 50)
            if i > 0 :
                linkScale = sn.input(0).name() + '.scale'
                before.knob('scale').setExpression(linkScale)
            before.setInput(0, sn.input(i))
            sn.setInput(i,before)
        else:
            print ('not connected')

    # Create node after selected node
    after = nuke.createNode('Reformat')
    after.knob('type').setValue(2)
    after.knob('resize').setValue(0)
    linkScale = '1/' + sn.input(0).name() + '.scale'
    print (linkScale)
    after.knob('scale').setExpression(linkScale)