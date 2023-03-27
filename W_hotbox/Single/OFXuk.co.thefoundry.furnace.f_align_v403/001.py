#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Export CornerPin
#
#----------------------------------------------------------------------------------------------------------

#http://www.nukepedia.com/python/import/export/f_aligntocornerpin
#by Frank Rueter
#www.ohufx.com

def F_AlignToCornerPin_export():
    fAlign = nuke.selectedNode()
    srcClip = fAlign.input(0)
    if not srcClip:
        nuke.message('{} src must be connected before exporting a CornerPin'.format(fAlign.name()))
        return

    c = nuke.nodes.CornerPin2D()
    c.setInput(0, srcClip)
    c['from1'].setValue((0,0))
    c['from2'].setValue((srcClip.width(),0))
    c['from3'].setValue((srcClip.width(),srcClip.height()))
    c['from4'].setValue((0,srcClip.height()))
    c['to1'].fromScript(fAlign['pinBL'].toScript())
    c['to2'].fromScript(fAlign['pinBR'].toScript())
    c['to3'].fromScript(fAlign['pinTR'].toScript())
    c['to4'].fromScript(fAlign['pinTL'].toScript())
    c['invert'].setValue(fAlign['invert'].value())
    c['label'].setValue('F_Align_Baked')


F_AlignToCornerPin_export()