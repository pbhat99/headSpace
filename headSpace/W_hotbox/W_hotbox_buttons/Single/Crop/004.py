#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Expand(+)
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    boxValue = i.knob('box').value()
    i.knob('box').setValue((boxValue[0]-20,boxValue[1]-20,boxValue[2]+20,boxValue[3]+20))