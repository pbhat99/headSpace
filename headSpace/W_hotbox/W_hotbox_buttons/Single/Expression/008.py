#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: NaN Fix
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('expr0').setValue('isnan (r) ? 0:r')
    i.knob('expr1').setValue('isnan (r) ? 0:g')
    i.knob('expr2').setValue('isnan (r) ? 0:b')
    i.knob('expr3').setValue('isnan (b) ? 0:a')
    i.knob('label').setValue('NaN fixed')