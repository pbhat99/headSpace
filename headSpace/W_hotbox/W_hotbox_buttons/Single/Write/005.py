#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Render this frame
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
        curFrame = int(nuke.knob("frame"))
        nuke.execute(i.name(), curFrame, curFrame)