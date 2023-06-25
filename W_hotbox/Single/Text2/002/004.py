#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: BR
#
#----------------------------------------------------------------------------------------------------------

safeArea = nuke.root()['format'].value().width()*.005+nuke.root()['format'].value().height()*.005


for i in nuke.selectedNodes():
    
    i.knob('xjustify').setValue('right')
    i.knob('yjustify').setValue('bottom')
    
    i.knob('box').setValue([safeArea,safeArea,nuke.root()['format'].value().width()-safeArea,nuke.root()['format'].value().height()-safeArea])