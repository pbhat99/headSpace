#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: nameCard
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    fname = i['file'].getValue().split('/')[-1].split('.')[0].split('_')
    fname = fname[5:-1]
    fname = '_'.join(fname)
    stickyNode = nuke.createNode('StickyNote')
    stickyNode.knob('label').setValue(fname)
    stickyNode.knob('note_font_size').setValue(200)
    stickyNode.knob('tile_color').setValue(1179010815)