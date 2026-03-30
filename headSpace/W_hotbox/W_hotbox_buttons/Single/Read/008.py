#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Localise
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('localizationPolicy').value() == 'off':
        i.knob('localizationPolicy').setValue('on')
    else:
        i.knob('localizationPolicy').setValue('off')