#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Next
#
#----------------------------------------------------------------------------------------------------------

L = nuke.layers()
for i in nuke.selectedNodes():
     inValue = i.knob("in").value()
     index = L.index(inValue) + 1
     if index >= len(L): index = 0
     nextIn = L[index]
     i.knob("in").setValue(nextIn)
     i.knob("label").setValue(nextIn)

