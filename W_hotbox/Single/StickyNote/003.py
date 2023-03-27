#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Paste
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
  try:
     from PySide2 import QtWidgets
  except:
     from PySide import QtGui as QtWidgets
  clipboard = str("<align=left>") + "\n" + QtWidgets.QApplication.clipboard().text()
  clipboard = clipboard.encode('utf-8')
  print (clipboard)

  i.knob('label').setValue(clipboard)


'''
from PySide import QtGui
clipboard = QtGui.QApplication.clipboard()
print clipboard.text() # show current clipboard contents
clipboard.setText("Yay") # set clipboard
'''