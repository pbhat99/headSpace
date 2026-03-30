#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Shot Name
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
        i.knob('message').setValue('[join [lrange [split [knob [topnode].file] _] 9 12] ]')
        
#1st underscore is split and last _ is join, from 9 to 12 list index