#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Supress G
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('expr0').setValue('')
    i.knob('expr1').setValue('g>(r+b)/2?(r+b)/2:g')
    i.knob('expr2').setValue('')
    i.knob('expr3').setValue('')
    i.knob('label').setValue('Supressed Green')
    i.knob('tile_color').setValue(2147450879)