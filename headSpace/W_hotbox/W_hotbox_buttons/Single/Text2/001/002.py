#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: topNode
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('message').setValue('[lindex [split [lindex [split [knob [topnode].file] .] 0] /] end]')
    #i.knob('message').setValue('[lrange [split [file tail [file rootname [metadata input/filename]]]  .] 0 0]')