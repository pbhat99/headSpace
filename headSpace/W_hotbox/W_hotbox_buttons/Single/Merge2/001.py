#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Screen/Plus
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('operation').value() == 'screen':
        i.knob('operation').setValue('plus')
        i.knob('output').setValue('rgb')
    else:
        i.knob('operation').setValue('screen')
        i.knob('output').setValue('rgba')