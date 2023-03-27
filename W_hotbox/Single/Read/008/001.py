#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: New
#
#----------------------------------------------------------------------------------------------------------

rvc = 'rv ' + nuke.selectedNode()["file"].value() + ' &'
print (rvc)
clipboard = QtWidgets.QApplication.clipboard()
clipboard.setText(rvc)
os.system('gnome-terminal')