#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Scale Up
#
#----------------------------------------------------------------------------------------------------------

def scaleUpCornerpin():

    selNode = None
    try:
      selNode = nuke.selectedNode()
    except ValueError:  # no node selected 
      pass

    if selNode is not None:
        selClass = selNode.Class()
        if selClass == 'CornerPin2D':
            to1x = selNode['to1'].getValue(0)
            selNode['to1'].setValue(to1x-10.0, 0)

            to1y = selNode['to1'].getValue(1)
            selNode['to1'].setValue(to1y-10.0, 1)

            to2x = selNode['to2'].getValue(0)
            selNode['to2'].setValue(to2x+10.0, 0)

            to2y = selNode['to2'].getValue(1)
            selNode['to2'].setValue(to2y-10.0, 1)


            to3x = selNode['to3'].getValue(0)
            selNode['to3'].setValue(to3x+10.0, 0)

            to3y = selNode['to3'].getValue(1)
            selNode['to3'].setValue(to3y+10.0, 1)

            to4x = selNode['to4'].getValue(0)
            selNode['to4'].setValue(to4x-10.0, 0)

            to4y = selNode['to4'].getValue(1)
            selNode['to4'].setValue(to4y+10.0, 1)
        else:
            return
            
scaleUpCornerpin()