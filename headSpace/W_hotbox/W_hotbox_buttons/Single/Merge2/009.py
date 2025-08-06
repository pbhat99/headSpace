#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: mix to multiply
#
#----------------------------------------------------------------------------------------------------------

for n in nuke.selectedNodes():
    mult = nuke.nodes.Multiply(xpos = n.xpos() + 100, ypos = n.ypos(), channels = 'rgba')
    mult['value'].fromScript(n['mix'].toScript())
    n['mix'].clearAnimated()
    n['mix'].setValue(1)