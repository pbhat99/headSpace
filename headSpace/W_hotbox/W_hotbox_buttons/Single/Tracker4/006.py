#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: export roto
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    rt = nuke.createNode('Roto')
    rt['translate'].fromScript(i['translate'].toScript())
    rt['rotate'].fromScript(i['rotate'].toScript())
    rt['scale'].fromScript(i['scale'].toScript())
    rt['center'].fromScript(i['center'].toScript())
    rt['opacity'].setValue(1)
    rt['label'].setValue('Tracked')