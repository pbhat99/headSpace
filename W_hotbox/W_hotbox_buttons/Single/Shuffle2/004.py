#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Alpha
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i['in1'].setValue('rgba')
    i["mappings"].setValue([('rgba.alpha', 'rgba.red'), ('rgba.alpha', 'rgba.green'),('rgba.alpha', 'rgba.blue'),('rgba.alpha', 'rgba.alpha')])

    i.knob('tile_color').setValue(0xffffffff)