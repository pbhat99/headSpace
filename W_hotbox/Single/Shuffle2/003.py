#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Red
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i['in1'].setValue('rgba')
    i["mappings"].setValue([('rgba.red', 'rgba.red'), ('rgba.red', 'rgba.green'),('rgba.red', 'rgba.blue'),('rgba.red', 'rgba.alpha')])

    i.knob('tile_color').setValue(3204448511)