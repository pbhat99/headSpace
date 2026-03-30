#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Close Groups
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.allNodes("Group"):
    i['show_group_view'].setValue(False)