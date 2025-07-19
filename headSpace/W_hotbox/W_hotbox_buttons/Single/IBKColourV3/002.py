#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Duplicate
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    newNode = nuke.createNode('IBKColourV3') 
    newNode.knob('screen_type').setValue(i.knob('screen_type').value())
    newNode.knob('off').setValue(i.knob('off').value())
    newNode.knob('mult').setValue(i.knob('mult').value())
    newNode.knob('multi').setValue(i.knob('multi').value()*2)