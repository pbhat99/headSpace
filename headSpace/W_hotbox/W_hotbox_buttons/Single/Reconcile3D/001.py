#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Extract transform
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
t = nuke.nodes.Transform()
t['position'].fromScript(i['output'].toScript())