#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: paste node
#
#----------------------------------------------------------------------------------------------------------

set cut_paste_input [stack 0]
version 10.0 v4
push $cut_paste_input
NoOp {
name NoOp1
knobChanged "if nuke.thisKnob().name() == 'inputChange':\n    nuke.message('Wait a minute... the input changed!')"
selected true
xpos 5671
ypos -4042
}