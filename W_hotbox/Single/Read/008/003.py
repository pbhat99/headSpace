#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Merge
#
#----------------------------------------------------------------------------------------------------------

rvc = 'rvpush merge ' + nuke.selectedNode()["file"].value() + ' &'
print (rvc)
clipboard = QtWidgets.QApplication.clipboard()
clipboard.setText(rvc)