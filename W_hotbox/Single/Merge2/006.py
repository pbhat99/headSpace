#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: rgb
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('Achannels').value() == 'alpha':
        i.knob('Achannels').setValue('rgba')
        i.knob('Bchannels').setValue('rgba')
    elif i.knob('Achannels').value() == 'rgba':
        i.knob('Bchannels').setValue('all')
        i.knob('Bchannels').setValue('all')
    else:
        i.knob('Achannels').setValue('alpha')