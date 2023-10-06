#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: toggle Clip
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('cliptype').value() == 'format':
        i.knob('cliptype').setValue('no clip')
    else:
        i.knob('cliptype').setValue('format')