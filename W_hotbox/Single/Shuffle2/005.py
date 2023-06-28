#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Next
#
#----------------------------------------------------------------------------------------------------------

L = nuke.layers()
for i in nuke.selectedNodes():
     inValue = i.knob("in1").value()
     index = L.index(inValue) + 1
     if index >= len(L): index = 0
     nextIn = L[index]
     i.knob("in1").setValue(nextIn)
     i.knob("label").setValue(nextIn)
