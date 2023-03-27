import nuke



#------------------------------------------------------------------------------
#  $GUI Toggle
#------------------------------------------------------------------------------
def disableGUI():
	for dis in nuke.selectedNodes():
		if dis['disable'].hasExpression():
			dis['disable'].clearAnimated()
			dis['disable'].setValue(0)
		else:
			dis['disable'].setExpression('[python {1-nuke.executing()}]')
	return




#------------------------------------------------------------------------------
#paste clipboard to stickyNote
#------------------------------------------------------------------------------
def pasteNote():
  try:
     from PySide2 import QtWidgets
  except:
     from PySide import QtGui as QtWidgets
  clipboard = str('<align=left>') + '\n' + QtWidgets.QApplication.clipboard().text()
  clipboard = clipboard.encode('utf-8')
     #copyClip = QtGui.QApplication.clipboard().setText("Yay")
  sn = nuke.createNode("StickyNote")
  sn.knob('label').setValue(clipboard)




#------------------------------------------------------------------------------
# label replaced by rename
#------------------------------------------------------------------------------
def nLabel():
    lbl = nuke.selectedNode().knob('label').getValue()
    txt = nuke.getInput('Change label', lbl)
    if txt:
        for n in nuke.selectedNodes():
            n['label'].setValue(txt)

