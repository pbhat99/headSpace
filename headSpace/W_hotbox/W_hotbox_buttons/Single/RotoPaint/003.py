#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Output Mask
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('outputMask').value() == 'none':
        i.knob('outputMask').setValue('mask.a')
    else:
        i.knob('outputMask').setValue('none')