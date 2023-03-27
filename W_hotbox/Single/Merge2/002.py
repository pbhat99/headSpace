#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Plus
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('operation').setValue('plus')
    i.knob('output').setValue('rgb')