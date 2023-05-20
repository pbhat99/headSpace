#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set IP
#
#----------------------------------------------------------------------------------------------------------

import nuke
def nextName(base_name):
    count = 1
    while nuke.exists(base_name+str(count)):
        count += 1
    return base_name+str(count)

sn = nuke.selectedNode()
try:
    vNode = nuke.toNode('VIEWER_INPUT')
    rname = nextName(vNode.Class())
    vNode['name'].setValue(rname)
except:
    pass
    
sn['name'].setValue('VIEWER_INPUT')
