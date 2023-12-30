#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: RC
#
#----------------------------------------------------------------------------------------------------------

safeArea = nuke.root()['format'].value().width()*.005+nuke.root()['format'].value().height()*.005

for i in nuke.selectedNodes():
    
    i.knob('xjustify').setValue('right')
    i.knob('yjustify').setValue('center')
    
    i.knob('box').setValue([safeArea,safeArea,nuke.root()['format'].value().width()-safeArea,nuke.root()['format'].value().height()-safeArea])