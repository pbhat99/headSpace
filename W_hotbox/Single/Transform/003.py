#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: MoBlur
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('shutteroffset').setValue("centered")
    invertKnob = i.knob('motionblur')
    invertKnob.setValue(1-int(invertKnob.value()))
