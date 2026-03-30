#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Group View
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    invertKnob = i.knob('disable_group_view')
    invertKnob.setValue(1-int(invertKnob.value()))