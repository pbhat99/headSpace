#----------------------------------------------------------------------------------------------------------
# Wouter Gilsing
# woutergilsing@hotmail.com
# March 2018
# v2.2
#----------------------------------------------------------------------------------------------------------

import nuke
import os
import math
from nukescripts import panels

#Choose between PySide, PySide2 and PySide6 based on Nuke version
if nuke.NUKE_VERSION_MAJOR < 11:
	from PySide import QtCore, QtGui, QtGui as QtWidgets
	QAction = QtGui.QAction
elif nuke.NUKE_VERSION_MAJOR >= 15:
	from PySide6 import QtGui, QtCore, QtWidgets
	QAction = QtGui.QAction
else:
	from PySide2 import QtGui, QtCore, QtWidgets
	QAction = QtWidgets.QAction

#----------------------------------------------------------------------------------------------------------
#Add to menu.py:
#----------------------------------------------------------------------------------------------------------
'''
import W_scaleTree
nukeMenu.addCommand('Edit/Node/W_scaleTree', 'W_scaleTree.scaleTreeFloatingPanel()', 'alt+`')
'''
#----------------------------------------------------------------------------------------------------------

#Location of the icons
#iconFolder = os.getenv('HOME') + '/.nuke/Scripts/W_scaleTree icons'
iconFolder = os.path.dirname(__file__) + '/W_scaleTree_icons'

#----------------------------------------------------------------------------------------------------------

class scaleTreeWidget(QtWidgets.QWidget):

    def __init__(self):

        super(scaleTreeWidget, self).__init__()

        self.setWindowTitle ('W_scaleTree')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumWidth(250)

        masterLayout = QtWidgets.QVBoxLayout()

        #--------------------------------------------------------------------------------------------------
        #Pivot manipulator
        #--------------------------------------------------------------------------------------------------

        self.setPivotWidget = pivotWidget()

        #add to layout
        pivotLayout = QtWidgets.QHBoxLayout()
        pivotLayout.addStretch()
        pivotLayout.addLayout(self.setPivotWidget)
        pivotLayout.addStretch()

        #--------------------------------------------------------------------------------------------------
        #Parameters
        #--------------------------------------------------------------------------------------------------

        self.ignore = True
        self.nodePositions = {}
        self.undo = None
        self.pivotX = 0
        self.pivotY = 0

        #--------------------------------------------------------------------------------------------------
        #Sliders
        #--------------------------------------------------------------------------------------------------

        sliderLayout = QtWidgets.QVBoxLayout()

        self.maxSlider = 200

        #uniform
        self.uniformSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.uniformSlider.setMinimum(0)
        self.uniformSlider.setMaximum(self.maxSlider)
        self.uniformSlider.setValue(self.maxSlider//2)

        self.uniformSlider.sliderPressed.connect(self.scanTree)
        self.uniformSlider.sliderMoved.connect(lambda: self.scaleTree(self.uniformSlider,['horizontal','vertical']))
        self.uniformSlider.sliderReleased.connect(self.resetSlider)

        #horizontal
        self.horizontalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(self.maxSlider)
        self.horizontalSlider.setValue(self.maxSlider//2)

        self.horizontalSlider.sliderPressed.connect(self.scanTree)
        self.horizontalSlider.valueChanged.connect(lambda: self.scaleTree(self.horizontalSlider,['horizontal']))
        self.horizontalSlider.sliderReleased.connect(self.resetSlider)

        #vertical
        self.verticalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(self.maxSlider)
        self.verticalSlider.setValue(self.maxSlider//2)

        self.verticalSlider.sliderPressed.connect(self.scanTree)
        self.verticalSlider.valueChanged.connect(lambda: self.scaleTree(self.verticalSlider,['vertical']))
        self.verticalSlider.sliderReleased.connect(self.resetSlider)

        #rotation
        self.rotationSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rotationSlider.setMinimum(-90)
        self.rotationSlider.setMaximum(90)
        self.rotationSlider.setValue(0)

        self.rotationSlider.sliderPressed.connect(self.scanTree)
        self.rotationSlider.valueChanged.connect(lambda: self.rotateTree(self.rotationSlider))
        self.rotationSlider.sliderReleased.connect(self.resetSlider)

        #add to layout
        sliderLayout.addSpacing(25)
        sliderLayout.addWidget(QtWidgets.QLabel('Uniform'))
        sliderLayout.addWidget(self.uniformSlider)
        sliderLayout.addSpacing(25)
        sliderLayout.addWidget(QtWidgets.QLabel('Horizontal'))
        sliderLayout.addWidget(self.horizontalSlider)
        sliderLayout.addWidget(QtWidgets.QLabel('Vertical'))
        sliderLayout.addWidget(self.verticalSlider)
        sliderLayout.addSpacing(25)
        sliderLayout.addWidget(QtWidgets.QLabel('Rotation'))
        sliderLayout.addWidget(self.rotationSlider)

        #--------------------------------------------------------------------------------------------------
        #Spacing
        #--------------------------------------------------------------------------------------------------
        distributionLayout = QtWidgets.QVBoxLayout()
        distributionButtonLayout = QtWidgets.QHBoxLayout()


        self.horizontalButton = QtWidgets.QPushButton('Horizontal')
        self.verticalButton = QtWidgets.QPushButton('Vertical')

        self.horizontalButton.clicked.connect(lambda: self.distributeEvenly('x'))
        self.verticalButton.clicked.connect(lambda: self.distributeEvenly('y'))

        distributionButtonLayout.addStretch()
        distributionButtonLayout.addWidget(self.horizontalButton)
        distributionButtonLayout.addSpacing(10)
        distributionButtonLayout.addWidget(self.verticalButton)
        distributionButtonLayout.addStretch()

        #mirror
        mirrorLayout = QtWidgets.QVBoxLayout()
        mirrorButtonLayout = QtWidgets.QHBoxLayout()

        self.mirrorXButton = QtWidgets.QPushButton('Mirror X')
        self.mirrorYButton = QtWidgets.QPushButton('Mirror Y')

        self.mirrorXButton.clicked.connect(lambda: self.mirrorTree('x'))
        self.mirrorYButton.clicked.connect(lambda: self.mirrorTree('y'))

        mirrorButtonLayout.addStretch()
        mirrorButtonLayout.addWidget(self.mirrorXButton)
        mirrorButtonLayout.addSpacing(10)
        mirrorButtonLayout.addWidget(self.mirrorYButton)
        mirrorButtonLayout.addStretch()

        mirrorLayout.addWidget(QtWidgets.QLabel('Mirror'))
        mirrorLayout.addLayout(mirrorButtonLayout)

        distributionLayout.addWidget(QtWidgets.QLabel('Distribute Evenly'))
        distributionLayout.addLayout(distributionButtonLayout)

        #--------------------------------------------------------------------------------------------------
        #Assamble UI
        #--------------------------------------------------------------------------------------------------

        masterLayout.addSpacing(25)
        masterLayout.addLayout(pivotLayout)
        masterLayout.addSpacing(25)
        masterLayout.addLayout(sliderLayout)
        masterLayout.addSpacing(25)
        masterLayout.addLayout(mirrorLayout)
        masterLayout.addSpacing(10)
        masterLayout.addLayout(distributionLayout)
        masterLayout.addSpacing(10)
        masterLayout.addStretch()

        self.setLayout(masterLayout)

        #--------------------------------------------------------------------------------------------------
        #Add shortcuts
        #--------------------------------------------------------------------------------------------------

        #quit
        try:
            self.closeAction = QAction(self)
            shortcut = nuke.menu('Nuke').findItem('Edit/Node/W_scaleTree').shortcut()
            self.closeAction.setShortcut(QtGui.QKeySequence(shortcut))
            self.closeAction.triggered.connect(self.close)
            self.addAction(self.closeAction)
        except:
            pass

        #corners

        self.setPivotActionTL = QAction(self)
        self.setPivotActionTR = QAction(self)
        self.setPivotActionBL = QAction(self)
        self.setPivotActionBR = QAction(self)

        self.setPivotActionTL.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_1))
        self.setPivotActionTR.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_2))
        self.setPivotActionBL.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_3))
        self.setPivotActionBR.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_4))

        self.setPivotActionTL.triggered.connect(lambda: self.setPivotWidget.allButtons[0].mouseReleaseEvent(''))
        self.setPivotActionTR.triggered.connect(lambda: self.setPivotWidget.allButtons[2].mouseReleaseEvent(''))
        self.setPivotActionBL.triggered.connect(lambda: self.setPivotWidget.allButtons[6].mouseReleaseEvent(''))
        self.setPivotActionBR.triggered.connect(lambda: self.setPivotWidget.allButtons[8].mouseReleaseEvent(''))

        self.addAction(self.setPivotActionTL)
        self.addAction(self.setPivotActionTR)
        self.addAction(self.setPivotActionBL)
        self.addAction(self.setPivotActionBR)

        #--------------------------------------------------------------------------------------------------

        #Spawn widget at current location of cursor
        self.adjustSize()
        self.move(QtGui.QCursor().pos() - QtCore.QPoint((self.width()//2),(self.height()//2)))

        #set pivot to center
        self.setPivotWidget.allButtons[4].mouseReleaseEvent('')

    def getDAG(self):
        '''
        Return the currently opened DAG in order to work correctly with groups.
        '''

        rootNode = nuke.Root()

        #collect all DAG's
        allDAGWidgets = [w for w in QtWidgets.QApplication.instance().allWidgets() if 'DAG' in w.objectName()]

        for w in allDAGWidgets:
            if w.isVisible():
                windowTitle = w.windowTitle()
                if windowTitle != 'Node Graph':
                    node = nuke.toNode(windowTitle.split(' ')[0])
                    if node:
                        rootNode = node
                        break

        return rootNode

    def getSelection(self):
        '''
    	Get selected nodes for active DAG.
    	'''

        with self.getDAG():
            selection = nuke.selectedNodes()

        return selection

    def scanTree(self):
        '''
        Calculate all need information regarding the current selection. Before doing any actual scaling.
        This method is called when the user starts dragging one of the sliders.
        '''
        


        selection = self.getSelection()

        #if there are less than two nodes selected. Don't do any scaling at all
        if len(selection) < 2:
            self.ignore = True
            self.undo = None
            return


        #Dictionary of all nodes with current position values. {[Node object] : (x pos, y position)}
        #Positions are all neutralized by taking the size of the node in account.

        self.nodePositions = {}

        allXpos = []
        allYpos = []

        for node in selection:

            #create lists and a dictionary storing position data
            if node.Class() != 'BackdropNode':

                x = node.xpos()+(node.screenWidth()/2)
                y = node.ypos()+(node.screenHeight()/2)

                self.nodePositions[node] = (x, y)

                allXpos.append(x)
                allYpos.append(y)

            else:
                #If a backdrop node is encountered, store the width and height as well as the regular position data.

                #store the nodes inside the backdrop in a list
                backdropSelection = node.getNodes()

                if len(backdropSelection) > 0:
                    allPositionData = [[n.xpos(), n.ypos(), n.screenWidth(), n.screenHeight()] for n in backdropSelection]

                    selectionX = min([pos[0]+(pos[2]/2) for pos in allPositionData])
                    selectionY = min([pos[1]+(pos[3]/2) for pos in allPositionData])

                    selectionW = max([pos[0]+(pos[2]/2) for pos in allPositionData])
                    selectionH = max([pos[1]+(pos[3]/2) for pos in allPositionData])

                    offsetX = node.xpos() - selectionX
                    offsetY = node.ypos() - selectionY
                    offsetW = (node.xpos() + node.knob('bdwidth').value()) - selectionW
                    offsetH = (node.ypos() + node.knob('bdheight').value()) - selectionH

                    self.nodePositions[node] = (selectionX, selectionY, selectionW, selectionH, offsetX, offsetY, offsetW, offsetH)

                    allXpos.append(selectionX)
                    allXpos.append(selectionW)
                    allYpos.append(selectionY)
                    allYpos.append(selectionH)

                else:
                    #if backdrop is empty, threat it as any other node
                    x = node.xpos()+(node.screenWidth()/2)
                    y = node.ypos()+(node.screenHeight()/2)

                    self.nodePositions[node] = (x, y)

                    allXpos.append(x)
                    allYpos.append(y)


        #calculate the most extreme values to define the borders of the selection
        minXpos = min(allXpos)
        maxXpos = max(allXpos)

        maxYpos = max(allYpos)
        minYpos = min(allYpos)

        #set the pivotpoint
        self.pivotX = (maxXpos * self.setPivotWidget.pivot[0]) + (minXpos * (1 - self.setPivotWidget.pivot[0]))
        self.pivotY = (maxYpos * self.setPivotWidget.pivot[1]) + (minYpos * (1 - self.setPivotWidget.pivot[1]))

        self.ignore = False

        #add the scaling of the nodes to the stack of preformed actions to offer the user the option to undo it.
        self.undo = nuke.Undo()
        self.undo.begin("Scale Nodes")

    def scaleTree(self, slider, mode):
        '''
        Scale the currently selected nodes.
        This method is called when the user is actually moving one of the sliders.
        '''

        if not self.ignore:

            multiplier = float(slider.value())/(self.maxSlider/2)
            #make the slider act exponential rather than linear when the value is above 1.
            if multiplier > 1:
                multiplier *= multiplier

            for i in self.nodePositions.keys():
                
                if len(self.nodePositions[i]) == 2:
                #wehn dealing with a backdrop node, not only adjust the postion but also the scale.

                    if 'horizontal' in mode:
                        screenWidth = i.screenWidth()/2
                        newPos = int((self.pivotX - ((self.pivotX - self.nodePositions[i][0]) * multiplier)) - screenWidth)
                        i.setXpos(newPos)
    
                    if 'vertical' in mode:
                        screenHeight = i.screenHeight()/2
                        newPos = int((self.pivotY - ((self.pivotY - self.nodePositions[i][1]) * multiplier)) - screenHeight)
                        i.setYpos(newPos)
                
                else:
                    if 'horizontal' in mode:

                        newPos = int(self.pivotX - ((self.pivotX - self.nodePositions[i][0]) * multiplier) + self.nodePositions[i][4])
                        newWidth = int(self.pivotX - ((self.pivotX - self.nodePositions[i][2]) * multiplier) + self.nodePositions[i][6] - newPos)

                        i.knob('bdwidth').setValue(newWidth)
                        i.setXpos(newPos)

                    if 'vertical' in mode:

                        newPos = int(self.pivotY - ((self.pivotY - self.nodePositions[i][1]) * multiplier) + self.nodePositions[i][5])
                        newHeight = int(self.pivotY - ((self.pivotY - self.nodePositions[i][3]) * multiplier) + self.nodePositions[i][7] - newPos)

                        i.knob('bdheight').setValue(newHeight)
                        i.setYpos(newPos)

    def rotateTree(self, slider):
        '''
        Rotate the currently selected nodes around the pivot.
        '''

        if not self.ignore:

            angle = float(slider.value())
            theta = math.radians(angle)

            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            for i in self.nodePositions.keys():
                
                if len(self.nodePositions[i]) == 2:
                    dx = self.nodePositions[i][0] - self.pivotX
                    dy = self.nodePositions[i][1] - self.pivotY

                    new_x = self.pivotX + (dx * cos_theta - dy * sin_theta)
                    new_y = self.pivotY + (dx * sin_theta + dy * cos_theta)

                    screenWidth = i.screenWidth() / 2
                    screenHeight = i.screenHeight() / 2

                    i.setXpos(int(new_x - screenWidth))
                    i.setYpos(int(new_y - screenHeight))
                
                else:
                    x1, y1 = self.nodePositions[i][0], self.nodePositions[i][1]
                    x2, y2 = self.nodePositions[i][2], self.nodePositions[i][3]
                    
                    corners = [
                        (x1, y1),
                        (x2, y1),
                        (x1, y2),
                        (x2, y2)
                    ]
                    
                    new_corners = []
                    for cx, cy in corners:
                        cdx = cx - self.pivotX
                        cdy = cy - self.pivotY
                        new_cx = self.pivotX + (cdx * cos_theta - cdy * sin_theta)
                        new_cy = self.pivotY + (cdx * sin_theta + cdy * cos_theta)
                        new_corners.append((new_cx, new_cy))
                        
                    min_x = min(c[0] for c in new_corners)
                    max_x = max(c[0] for c in new_corners)
                    min_y = min(c[1] for c in new_corners)
                    max_y = max(c[1] for c in new_corners)
                    
                    newPos_x = int(min_x + self.nodePositions[i][4])
                    newPos_y = int(min_y + self.nodePositions[i][5])
                    newWidth = int(max_x + self.nodePositions[i][6] - newPos_x)
                    newHeight = int(max_y + self.nodePositions[i][7] - newPos_y)
                    
                    i.knob('bdwidth').setValue(newWidth)
                    i.knob('bdheight').setValue(newHeight)
                    i.setXpos(newPos_x)
                    i.setYpos(newPos_y)

    def mirrorTree(self, axis):
        '''
        Mirror the currently selected nodes around the pivot.
        '''

        self.scanTree()

        if self.ignore:
            return

        #change undo name
        self.undo.end()
        self.undo = nuke.Undo()
        self.undo.begin("Mirror Nodes " + axis.upper())

        multiplier = -1.0

        for i in self.nodePositions.keys():
            if len(self.nodePositions[i]) == 2:
                if axis == 'x':
                    screenWidth = i.screenWidth()/2
                    newPos = int(self.pivotX - ((self.pivotX - self.nodePositions[i][0]) * multiplier) - screenWidth)
                    i.setXpos(newPos)
                else:
                    screenHeight = i.screenHeight()/2
                    newPos = int(self.pivotY - ((self.pivotY - self.nodePositions[i][1]) * multiplier) - screenHeight)
                    i.setYpos(newPos)
            else:
                if axis == 'x':
                    x1 = int(self.pivotX - ((self.pivotX - self.nodePositions[i][0]) * multiplier) + self.nodePositions[i][4])
                    x2 = int(self.pivotX - ((self.pivotX - self.nodePositions[i][2]) * multiplier) + self.nodePositions[i][6])
                    newPos = min(x1, x2)
                    newWidth = max(x1, x2) - newPos
                    i.knob('bdwidth').setValue(newWidth)
                    i.setXpos(newPos)
                else:
                    y1 = int(self.pivotY - ((self.pivotY - self.nodePositions[i][1]) * multiplier) + self.nodePositions[i][5])
                    y2 = int(self.pivotY - ((self.pivotY - self.nodePositions[i][3]) * multiplier) + self.nodePositions[i][7])
                    newPos = min(y1, y2)
                    newHeight = max(y1, y2) - newPos
                    i.knob('bdheight').setValue(newHeight)
                    i.setYpos(newPos)

        self.undo.end()
        self.undo = None

    def resetSlider(self):
        #reset the sliders when the user releases the mouse.
        #use the ignore variable to make sure the nodes in the DAG are not affected by this.

        currentIgnoreValue = self.ignore
        self.ignore = True
        self.uniformSlider.setValue(self.maxSlider//2)
        self.horizontalSlider.setValue(self.maxSlider//2)
        self.verticalSlider.setValue(self.maxSlider//2)
        self.rotationSlider.setValue(0)
        self.ignore = currentIgnoreValue

        if self.undo:
            self.undo.end()

    def getScreenSize(self,node,axis):
        if axis == 'x':
            return node.screenWidth()/2
        else:
            return node.screenHeight()/2

    def distributeEvenly(self,axis):
        '''
        Equalize the amount of space between selected nodes.
        '''

        selection = self.getSelection()

        allPositionsDict = {}

        for node in selection:

            position = float(node.knob(axis+'pos').value() + self.getScreenSize(node,axis))

            if position in allPositionsDict.keys():
                allPositionsDict[position].append(node)
            else:
                allPositionsDict[position] = [node]

        allPositions = sorted(allPositionsDict.keys())

        amount = len(allPositions)
        if amount < 3:
            return

        minPos = allPositions[0]
        maxPos = allPositions[-1]

        stepSize = (maxPos - minPos) / (amount -1)

        self.undo = nuke.Undo()
        self.undo.begin("Distribute evenly")

        for index, i in enumerate(allPositions):
            newPos = minPos + index * stepSize
            for node in allPositionsDict[i]:

                node.knob(axis+'pos').setValue(int(newPos- self.getScreenSize(node,axis)))

        self.undo.end()
        self.undo = None
        
#----------------------------------------------------------------------------------------------------------

class pivotWidget(QtWidgets.QGridLayout):
    '''
    A widget that let's the user interactivaly set a pivot point fro where the nodes in the DAG will be scaled.
    '''
    def __init__(self):
        super(pivotWidget, self).__init__()

        self.allButtons = []

        self.setSpacing(0)
        for i in range(9):
            button = pivotButton(self,i)
            self.addWidget(button,i//3,i%3)
            self.allButtons.append(button)

        self.pivot = (.5,.5)


    def updateButtons(self,buttonID):
        for i in self.allButtons:
            i.update(buttonID)

#----------------------------------------------------------------------------------------------------------

class pivotButton(QtWidgets.QLabel):
    '''
    The buttons that are used to built the pivotWidget.
    '''
    def __init__(self, parent, position):
        super(pivotButton, self).__init__()

        self.parent = parent
        self.position = position

        #make sure the path to the icon folder doesn't end with a slash
        global iconFolder
        while iconFolder[-1] == '/':
            iconFolder = iconFolder[:-1]

        self.imageFile = '%s/W_scaleTree_pivotArrow_%i.png'%(iconFolder,position)

        self.setPixmap(QtGui.QPixmap(self.imageFile))

    def mouseReleaseEvent(self,event):
        #set pivot
        self.parent.updateButtons(self.position)
        self.parent.pivot = [(self.position%3)/2.0,(self.position//3)/2.0]

    def update(self,buttonID):
        '''
        Change the icon of the buttons when the user changes the pivot.
        '''

        #the button in the center of the widget has index 4
        offset = 4 - buttonID

        newPosition = self.position + offset

        #when placing the pivot in one of the side tiles,
        #tiles will reappear on the other side of the widget (like snake)
        #make sure that doesn't happen by forcing those tiles to be empty.
        for i in [ [0,3,6], [2,5,8] ]:
            if buttonID in i and newPosition in i:
                newPosition = 9
                break

        #there are only 9 icons (9 being an empty tile).
        #if a button ends up getting a new postion outside this range,
        #force those tiles to be empty.
        if newPosition not in range(9):
            newPosition = 9

        #set new icons
        self.imageFile = '%s/W_scaleTree_pivotArrow_%i.png'%(iconFolder,newPosition)
        self.setPixmap(QtGui.QPixmap(self.imageFile))

#----------------------------------------------------------------------------------------------------------
#Floating Panel
#----------------------------------------------------------------------------------------------------------

scaleTreeWidgetInstance = None
def scaleTreeFloatingPanel():
    global scaleTreeWidgetInstance
    if scaleTreeWidgetInstance != None:
        try:
            scaleTreeWidgetInstance.close()
        except:
            pass

    scaleTreeWidgetInstance = scaleTreeWidget()
    scaleTreeWidgetInstance.show()

#----------------------------------------------------------------------------------------------------------
#Docked Panel
#----------------------------------------------------------------------------------------------------------

panels.registerWidgetAsPanel('W_scaleTree.scaleTreeWidget', 'W_scaleTree', 'W_scaleTree.widget')

#----------------------------------------------------------------------------------------------------------