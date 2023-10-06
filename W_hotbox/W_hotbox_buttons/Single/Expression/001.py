#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Supress R
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('expr0').setValue('r>(g+b)/2?(g+b)/2:r')
    i.knob('expr1').setValue('')
    i.knob('expr2').setValue('')
    i.knob('expr3').setValue('')
    i.knob('label').setValue('Supressed Red')
    i.knob('tile_color').setValue(4286545919)