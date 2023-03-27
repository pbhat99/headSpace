#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: hide input
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
        i.knob('hide_input').setValue('[exists input0] ? 1 : 0')