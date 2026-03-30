#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Date
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
        i.knob('message').setValue('[clock format [clock seconds] -format "%d-%m-%Y"]')