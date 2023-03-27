#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: replace text
#
#----------------------------------------------------------------------------------------------------------

nuke.thisNode()["file"].setValue(nuke.root().name().replace("scripts","renders").replace(".nk",".mov"))