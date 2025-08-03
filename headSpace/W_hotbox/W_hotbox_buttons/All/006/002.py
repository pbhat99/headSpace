#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: lin | log
#
#----------------------------------------------------------------------------------------------------------

sn = nuke.selectedNode()
if sn:
    for i in range(sn.inputs()):
        if sn.input(i):
            before = nuke.nodes.OCIOLogConvert(operation = 1, xpos = sn.xpos()+ (-100*i), ypos = sn.ypos() - 50)
            before.setInput(0, sn.input(i))
            sn.setInput(i,before)
        else:
            print ('not connected')

    # Create node after selected node
    after = nuke.createNode('OCIOLogConvert')
    after.knob('operation').setValue(0)