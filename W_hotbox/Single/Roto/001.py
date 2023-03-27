#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: rgba/alpha
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('output').value() == 'alpha':
        i.knob('output').setValue('rgba')
    else:
        i.knob('output').setValue('alpha')