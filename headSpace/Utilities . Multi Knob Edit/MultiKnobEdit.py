# author: thorsten loeffler
# mail: thorsten.loeffler@gmail.com
# created this tool for http://www.woodblock.tv
# update to run under Nuke 11 (see PySide2)



# this script is basically a proofe of concept of a nice Softimage feature
# import this script and run multiEditExec(), afterwarts the multiknob edit mode is activate
# so all selected nodes of the same class will get the same value for the recently changed knob

# only static values are supported


import nuke

try:
    from PySide import QtGui, QtCore 
    qt_dialog = QtGui.QDialog
    qt_vbox_layout = QtGui.QVBoxLayout
    qt_label = QtGui.QLabel
    qt_application = QtGui.QApplication
    qt_focus = QtGui.QFocusFrame
except:
    from PySide2 import QtGui, QtCore, QtWidgets
    qt_dialog = QtWidgets.QDialog
    qt_vbox_layout = QtWidgets.QVBoxLayout
    qt_label = QtWidgets.QLabel
    qt_application = QtWidgets.QApplication
    qt_focus = QtWidgets.QFocusFrame

class toolStatusInfoMessage( qt_dialog ):

    def __init__(self, parent):
        super(toolStatusInfoMessage, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
        main_layout = qt_vbox_layout()
        label = qt_label("<font color=red size=4>multi knob edit mode activated</font>")
        main_layout.addWidget(label)
        self.setLayout(main_layout)
        self.setStyleSheet( 'QDialog{border:1px solid red}' )

excludes_list = [
    'xpos',
    'ypos',
    'name',
    'selected',
    'hidePanel',
    'showPanel'
]

multi_knob_edit_mode = False
tool_info = None

def getAllSelectedNodes():
    nodes = []
    for node in nuke.selectedNodes():
        if node.Class() != 'Group':
            nodes.append(node)
        elif node.Class() == 'Group':
            for node_in_group in node.nodes():
                nodes.append(node_in_group)
    return nodes


def editSameClassKnobs():
    if nuke.thisKnob():
        if nuke.thisKnob().name() not in excludes_list:
            for node in getAllSelectedNodes():
                if node.Class() == nuke.thisNode().Class():
                    if node[ nuke.thisKnob().name() ].isAnimated() == False:
                        node[ nuke.thisKnob().name() ].setValue( nuke.thisKnob().value() )
                        if nuke.thisKnob().Class() == 'LookupCurves_Knob':
                            node[ nuke.thisKnob().name() ].fromScript( nuke.thisKnob().toScript() )


def multiEditExec():
    #main funktion to run
    global multi_knob_edit_mode, tool_info
    parent = qt_application.activeWindow()
    if tool_info == None:
        tool_info = toolStatusInfoMessage( parent )
    tool_info.setGeometry( parent.frameGeometry().left() + ( parent.frameGeometry().width() / 2.0 ), parent.frameGeometry().top() + 10 , 0, 0 )
    qt_focus( parent )
    nuke.removeKnobChanged(editSameClassKnobs)
    if multi_knob_edit_mode == False:
        print ('multi knob edit mode activated')
        nuke.addKnobChanged(editSameClassKnobs)
        multi_knob_edit_mode = True
        tool_info.show()
    elif multi_knob_edit_mode == True:
        print ('multi knob edit mode deactivated')
        nuke.removeKnobChanged(editSameClassKnobs)
        multi_knob_edit_mode = False
        tool_info.close()
