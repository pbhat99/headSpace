#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: \ to /
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    f = i.knob('file').value()
    f = f.replace('\\', '/').replace('\a', '/a')
    i.knob('file').setValue(f)
print (f)