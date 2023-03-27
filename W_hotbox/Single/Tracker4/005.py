#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Export Paint
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    rt = nuke.createNode('RotoPaint')
    rt['translate'].fromScript(i['translate'].toScript())
    rt['rotate'].fromScript(i['rotate'].toScript())
    rt['scale'].fromScript(i['scale'].toScript())
    rt['center'].fromScript(i['center'].toScript())
    rt['opacity'].setValue(1)
    rt['label'].setValue('Tracked')