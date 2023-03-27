#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: set animated
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    curValueto1 = i.knob('to1').value()
    curValueto2 = i.knob('to2').value()
    curValueto3 = i.knob('to3').value()
    curValueto4 = i.knob('to4').value()
    
    i.knob('to1').setAnimated()
    i.knob('to2').setAnimated()
    i.knob('to3').setAnimated()
    i.knob('to4').setAnimated()
    
    curValue = i.knob('to1').setValue(curValueto1)
    curValue = i.knob('to2').setValue(curValueto2)
    curValue = i.knob('to3').setValue(curValueto3)
    curValue = i.knob('to4').setValue(curValueto4)