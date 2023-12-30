#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: from r/g/b/a
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('from0').value() == 'rgba.alpha':
        i.knob('from0').setValue('rgba.red')
    elif i.knob('from0').value() == 'rgba.red':
        i.knob('from0').setValue('rgba.green')
    elif i.knob('from0').value() == 'rgba.green':
        i.knob('from0').setValue('rgba.blue')
    else:
        i.knob('from0').setValue('rgba.alpha')