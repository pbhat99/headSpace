#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: rgb/a
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('channels').value() == 'rgba':
        i.knob('channels').setValue('rgb')
    elif i.knob('channels').value() == 'rgb':
        i.knob('channels').setValue('rgba')
    else:
        pass