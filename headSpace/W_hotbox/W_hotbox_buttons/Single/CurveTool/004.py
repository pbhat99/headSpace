#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: AutoCrop
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    
    first_frame = nuke.root().firstFrame()
    last_frame = nuke.root().lastFrame()

    i.knob('operation').setValue('Auto Crop')
    i.knob('go').execute()