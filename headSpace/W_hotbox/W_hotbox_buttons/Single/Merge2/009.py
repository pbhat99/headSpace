#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: mix to multiply
#
#----------------------------------------------------------------------------------------------------------

for n in nuke.selectedNodes():
    mult = nuke.nodes.Multiply(xpos = n.xpos() - 150, ypos = n.ypos(), channels = 'rgba')
    mult.setInput(0, n.input(1))
    n.setInput(1, mult)
    mult['value'].fromScript(n['mix'].toScript())
    n['mix'].clearAnimated()
    n['mix'].setValue(1)