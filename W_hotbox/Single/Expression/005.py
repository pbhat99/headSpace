#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: uv
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('expr0').setValue('(x+0.5)/width')
    i.knob('expr1').setValue('(y+0.5)/height')
    i.knob('expr2').setValue('0')
    i.knob('expr3').setValue('0')
    i.knob('label').setValue('uv')
    i.knob('tile_color').setValue(4278124285)