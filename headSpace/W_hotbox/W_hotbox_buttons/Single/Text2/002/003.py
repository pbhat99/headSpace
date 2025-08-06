#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: scriptName
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
        i.knob('message').setValue("[lindex [split [file rootname [python nuke.root().knob('name').value()]] /] end]")