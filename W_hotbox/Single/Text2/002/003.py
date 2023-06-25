#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: TR
#
#----------------------------------------------------------------------------------------------------------

safeArea = nuke.root()['format'].value().width()*.005+nuke.root()['format'].value().height()*.005

for i in nuke.selectedNodes():
    
    i.knob('xjustify').setValue('right')
    i.knob('yjustify').setValue('top')
    
    i.knob('box').setValue([safeArea,safeArea,nuke.root()['format'].value().width()-safeArea,nuke.root()['format'].value().height()-safeArea])