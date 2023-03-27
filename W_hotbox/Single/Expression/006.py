#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: uv to vector
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('expr0').setValue('-x+r*width-0.5')
    i.knob('expr1').setValue('(y+0.5)/height')
    i.knob('expr2').setValue('0')
    i.knob('expr3').setValue('0')
    i.knob('label').setValue('uv to vector')
    i.knob('tile_color').setValue(4278124285)