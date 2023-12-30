#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Blue
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i['in1'].setValue('rgba')
    
    i["mappings"].setValue([('rgba.blue', 'rgba.red'), ('rgba.blue', 'rgba.green'),('rgba.blue', 'rgba.blue'),('rgba.blue', 'rgba.alpha')])
    
    i.knob('tile_color').setValue(4177919)