#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Denoise
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    topnode_name = nuke.tcl("full_name [topnode %s]" % i.name())
    topnode = nuke.toNode(topnode_name)
    filepath = topnode['file'].value()
    filepath = filepath.replace("4096x2160", "Denoised")
    i.knob('file').setValue(filepath)
