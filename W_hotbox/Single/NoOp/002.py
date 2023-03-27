#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: dissable on input
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
        i.knob('label').setValue('[exists input0] ? 1 : 0')