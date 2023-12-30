#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Supress B
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('expr0').setValue('')
    i.knob('expr1').setValue('')
    i.knob('expr2').setValue('b>(r+g)/2?(r+g)/2:b')
    i.knob('expr3').setValue('')
    i.knob('label').setValue('Supressed Blue')
    i.knob('tile_color').setValue(2139095039)