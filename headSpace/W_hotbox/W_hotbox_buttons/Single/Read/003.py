#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Rename
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():

    path =  i.knob('file').value()
    path = path.split('/')[-1]
    path = path.split('.')[0]
    print path
    i.knob('name').setValue(path)
