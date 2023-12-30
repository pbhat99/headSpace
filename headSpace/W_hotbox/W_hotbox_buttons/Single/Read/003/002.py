#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Copy Path
#
#----------------------------------------------------------------------------------------------------------

x = '\n\n'
for i in nuke.selectedNodes():
    fl = i.knob('file').value()
    f = fl.split('/')[-2].split('_')[1] + ':\n\n' + fl
    x = x + f
print (x)
 
clipboard = QtWidgets.QApplication.clipboard()
clipboard.setText(f)