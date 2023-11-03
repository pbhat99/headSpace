import nuke
import nukescripts
import time
import threading


#------------------------------------------------------------------------------
#  $GUI Toggle
#------------------------------------------------------------------------------
def disableGUI():
    for dis in nuke.selectedNodes():
        if dis['disable'].hasExpression():
            dis['disable'].clearAnimated()
            dis['disable'].setValue(0)
        else:
            dis['disable'].setExpression('$gui') # for general use
            #dis['disable'].setExpression('[python {1-nuke.executing()}]') # if u need local render support
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
    for n in nuke.selectedNodes():
        n['label'].setValue(txt)
        if n.Class() == 'Dot':
            n['note_font_size'].setValue(55)
        elif n.Class() == 'BackdropNode' or n.Class() == 'StickyNote':
            n['note_font_size'].setValue(200)
        else:
            pass



def openWeb(webLink):
    from webbrowser import open as openUrl
    openUrl(webLink)


def openDoc(docLink):
    webbrowser.open(docLink)


# def convert2decimal(num):
#     if num % 1 == 0:
#         num = "{0:0.0f}".format(num)
#     else:
#         num = "{0:.2f}".format(num).rstrip("-0b").rstrip("-.b")
#     return num