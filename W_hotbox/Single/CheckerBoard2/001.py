#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Toggle Centerline
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('centerlinewidth').setValue(3-i.knob('centerlinewidth').value())