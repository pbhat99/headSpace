#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Green
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i['in1'].setValue('rgba')
    
    i["mappings"].setValue([('rgba.green', 'rgba.red'), ('rgba.green', 'rgba.green'),('rgba.green', 'rgba.blue'),('rgba.green', 'rgba.alpha')])
    
    i.knob('tile_color').setValue(12517631)