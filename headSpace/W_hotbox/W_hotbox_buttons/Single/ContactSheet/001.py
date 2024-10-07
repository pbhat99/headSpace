#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Auto Fit
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
      i.knob('width').setValue(nuke.root().format().width())
      i.knob('height').setValue(nuke.root().format().height())
      i.knob('center').setValue('true')
      i.knob('rows').setExpression('ceil(inputs/columns)')
      i.knob('columns').setExpression('ceil(sqrt(inputs))')