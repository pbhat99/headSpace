#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Auto Fit
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
  i.knob('rows').setExpression('ceil(inputs/columns)')
  i.knob('columns').setExpression('ceil(sqrt(inputs))')
  i.knob('center').setValue('true')