#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Mov Write
#
#----------------------------------------------------------------------------------------------------------

dirPath = nuke.getFilename('Get File Contents', '')
for i in nuke.selectedNodes():
    if dirPath == None :
        f = i.knob('file').value().replace('%04d.exr','mov')
    else:
        f = dirPath + i.knob('file').value().split('/')[-1].replace('%04d.exr','mov')
    print f
    ww = nuke.createNode("Write")
    ww.setInput(0,i)
    ww.knob('file').setValue(f)
    ww.knob('colorspace').setValue('MillView')
    print (i)