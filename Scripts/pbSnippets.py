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
    if txt:
        for n in nuke.selectedNodes():
            n['label'].setValue(txt)




#------------------------------------------------------------------------------
# Gizmo to group convert & replace by Victor Perez
#------------------------------------------------------------------------------
def convertGizmosToGroups():
   ###Node Selections
   nodeSelection = nuke.selectedNodes()
   noGizmoSelection = []
   gizmoSelection = []
   for n in nodeSelection:
       if 'gizmo_file' in n.knobs():
           gizmoSelection.append(n)
       else:
           noGizmoSelection.append(n)
   groupSelection = []

   for n in gizmoSelection:
       bypassGroup = False
       ###Current Status Variables
       nodeName = n.knob('name').value()
       nodeXPosition = n['xpos'].value()
       nodeYPosition = n['ypos'].value()
       nodeHideInput = n.knob('hide_input').value()
       nodeCached = n.knob('cached').value()
       nodePostageStamp = n.knob('postage_stamp').value()
       nodeDisable = n.knob('disable').value()
       nodeDopeSheet = n.knob('dope_sheet').value()
       nodeDependencies = n.dependencies()
       nodeMaxInputs = n.maxInputs()
       inputsList = []

       ###Current Node Isolate Selection
       for i in nodeSelection:
           i.knob('selected').setValue(False)            
       n.knob('selected').setValue(True)

       nuke.tcl('copy_gizmo_to_group [selected_node]')

       ###Refresh selections
       groupSelection.append(nuke.selectedNode())
       newGroup = nuke.selectedNode()

       ###Paste Attributes
       newGroup.knob('xpos').setValue(nodeXPosition)
       newGroup.knob('ypos').setValue(nodeYPosition)
       newGroup.knob('hide_input').setValue(nodeHideInput)
       newGroup.knob('cached').setValue(nodeCached)
       newGroup.knob('postage_stamp').setValue(nodePostageStamp)
       newGroup.knob('disable').setValue(nodeDisable)
       newGroup.knob('dope_sheet').setValue(nodeDopeSheet)

       ###Connect Inputs
       for f in range(0, nodeMaxInputs):
           inputsList.append(n.input(f))
       for num, r in enumerate(inputsList):
           newGroup.setInput(num, None)
       for num, s in enumerate(inputsList):
           newGroup.setInput(num, s)

       n.knob('name').setValue('temp__'+nodeName+'__temp')
       newGroup.knob('name').setValue(nodeName)

       newGroup.knob('selected').setValue(False)

   ###Cleanup (remove gizmos, leave groups)
   for y in gizmoSelection:
       y.knob('selected').setValue(True)
   nukescripts.node_delete(popupOnError=False)
   for z in groupSelection:
       z.knob('selected').setValue(True)
   for w in noGizmoSelection:
       w.knob('selected').setValue(True)





#------------------------------------------------------------------------------
# Mirror nodes by Frank Rueter
#------------------------------------------------------------------------------
try:
    range = xrange
except:
    pass

class MirrorNodes( threading.Thread ):
    def __init__(self, nodes, direction='x', axis='average'):
        threading.Thread.__init__( self )
        if len( nodes ) < 2:
            raise ValueError("At least two nodes have to be selected")
        if direction.lower() not in ('x', 'y'):
            raise ValueError("direction argument must be x or y")
        
        self.axis = axis
        self.posDict = {}
        self.nodes= nodes
        self.direction = direction
        self.__mirrorPos()
        
    #----------------------------------
    def __mirrorPos(self):
        '''Get the mirrored position for each node'''
        if self.direction == 'x':
            if self.axis == 'last':
                n = nuke.selectedNodes()[0]
                axis = float(n.xpos() + n.screenWidth() / 2)
            elif self.axis == 'first':
                n = nuke.selectedNodes()[-1]
                axis = float(n.xpos() + n.screenWidth() / 2)
            else:
                # use average
                positions = [n.xpos() + n.screenWidth() / 2 for n in self.nodes]
                axis = float(sum(positions)) / len(positions)
        else:
            if self.axis == 'last':
                n = nuke.selectedNodes()[0]
                axis = float(n.ypos() + n.screenHeight() / 2)
            elif self.axis == 'first':
                n = nuke.selectedNodes()[-1]
                axis = float(n.ypos() + n.screenHeight() / 2)
            else:
                # use average
                positions = [n.ypos() + n.screenHeight() / 2 for n in self.nodes]
                axis = float(sum(positions)) / len(positions)            

        for n in self.nodes:
            if self.direction == 'x':
                centrePos = n.xpos() + n.screenWidth()/2
                oldPos = n.xpos()
                newPos = centrePos - 2*( centrePos - axis ) - n.screenWidth()/2.0
            else:
                centrePos = n.ypos() + n.screenHeight()/2
                oldPos = n.ypos()
                newPos = centrePos - 2*( centrePos - axis ) - n.screenHeight()/2.0
            self.posDict[ n ] = ( oldPos, round( newPos ) )

    #----------------------------------
    def run( self ):
        incs = 10
        for i in range( incs ):
            for n in self.nodes:
                oldPos = self.posDict[ n ][ 0 ]
                newPos = self.posDict[ n ][ 1 ]
                curPos = oldPos + ( newPos - oldPos ) / incs * (i+1)
                if self.direction == 'x':
                    nuke.executeInMainThreadWithResult( n.setXpos, int(curPos) )
                else:
                    nuke.executeInMainThreadWithResult( n.setYpos, int(curPos) )
            time.sleep(.02)