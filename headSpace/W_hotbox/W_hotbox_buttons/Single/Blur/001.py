#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Alpha for roto
#
#----------------------------------------------------------------------------------------------------------

for sel in nuke.allNodes('Roto'):
    for each in sel.dependent():
        if each.Class()=="Blur":
            each['channels'].setValue("alpha")