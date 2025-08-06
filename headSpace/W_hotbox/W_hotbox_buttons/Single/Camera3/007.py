#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: ImagePlane
#
#----------------------------------------------------------------------------------------------------------

for n in nuke.selectedNodes():
    card = nuke.nodes.Card2(xpos = n.xpos() + 100, ypos = n.ypos(),z = 10, rows = 2, columns = 2)
    tgeo = nuke.nodes.TransformGeo(xpos = card.xpos(), ypos = card.ypos() + 35)
    card['lens_in_focal'].setExpression(n.name() + '.focal')
    card['lens_in_haperture'].setExpression(n.name() + '.haperture')
    tgeo.setInput(0,card)
    tgeo.setInput(1,n)