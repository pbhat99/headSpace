mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Nudge Nodes UP', 'import transformNodesTools ; transformNodesTools.nudgeNodes_up()','Ctrl+Alt+UP')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Nudge Nodes DOWN', 'import transformNodesTools ; transformNodesTools.nudgeNodes_down()','Ctrl+Alt+DOWN')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Nudge Nodes LEFT', 'import transformNodesTools ; transformNodesTools.nudgeNodes_left()','Ctrl+Alt+LEFT')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Nudge Nodes RIGHT', 'import transformNodesTools ; transformNodesTools.nudgeNodes_right()','Ctrl+Alt+RIGHT')

nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Nudge Nodes UP MORE', 'import transformNodesTools ; transformNodesTools.nudgeNodes_up_more()','Shift+Ctrl+Alt+UP')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Nudge Nodes DOWN MORE', 'import transformNodesTools ; transformNodesTools.nudgeNodes_down_more()','Shift+Ctrl+Alt+DOWN')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Nudge Nodes LEFT MORE', 'import transformNodesTools ; transformNodesTools.nudgeNodes_left_more()','Shift+Ctrl+Alt+LEFT')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Nudge Nodes RIGHT MORE', 'import transformNodesTools ; transformNodesTools.nudgeNodes_right_more()','Shift+Ctrl+Alt+RIGHT')

nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Scale down Nodes', 'import transformNodesTools ; transformNodesTools.scaleNodePositionsInXandY()','Ctrl+Alt+i')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Scale down Nodes X only', 'import transformNodesTools ; transformNodesTools.scaleNodePositionsInXonly()','Ctrl+Alt+x')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Scale down Nodes Y only', 'import transformNodesTools ; transformNodesTools.scaleNodePositionsInYonly()','Ctrl+Alt+y')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Scale up Nodes', 'import transformNodesTools ; transformNodesTools.scaleNodePositionsOutXandY()','Ctrl+Alt+o')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Scale up Nodes X only', 'import transformNodesTools ; transformNodesTools.scaleNodePositionsOutXonly()','Shift+Ctrl+Alt+x')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Scale up Nodes Y only', 'import transformNodesTools ; transformNodesTools.scaleNodePositionsOutYonly()','Shift+Ctrl+Alt+y')

nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Rotate Nodes Clockwise', 'import transformNodesTools ; transformNodesTools.rotateNodes90DegreesCW()','Ctrl+Alt+r')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Rotate Nodes CounterClockwise', 'import transformNodesTools ; transformNodesTools.rotateNodes90DegreesCCW()','Shift+Ctrl+Alt+r')

nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Mirror Nodes X', 'import transformNodesTools ; transformNodesTools.mirrorX()','Ctrl+Alt+w')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Mirror Nodes Y', 'import transformNodesTools ; transformNodesTools.mirrorY()','Shift+Ctrl+Alt+w')

nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Create Transform Pivot-Dot', 'import transformNodesTools ; transformNodesTools.createPivotDot()','Ctrl+Alt+p')
nuke.menu("Nuke").addCommand(mainMenu + 'Move Nodes/Delete Transform Pivot-Dot', 'import transformNodesTools ; transformNodesTools.deletePivotDot()','Shift+Ctrl+Alt+p')


nuke.menu("Nuke").addCommand(mainMenu + 'Select Nodes/Select SelectionSet 01 Nodes', 'import transformNodesTools ; transformNodesTools.selectSelectionSet_Nodes(1)')

nuke.menu("Nuke").addCommand(mainMenu + 'Select Nodes/Add selected Nodes to SelectionSet 02', 'import transformNodesTools ; transformNodesTools.addSelectionToSelectionSet(2)')
nuke.menu("Nuke").addCommand(mainMenu + 'Select Nodes/Select SelectionSet 02 Nodes', 'import transformNodesTools ; transformNodesTools.selectSelectionSet_Nodes(2)')

nuke.menu("Nuke").addCommand(mainMenu + 'Select Nodes/Add selected Nodes to SelectionSet 03', 'import transformNodesTools ; transformNodesTools.addSelectionToSelectionSet(3)')
nuke.menu("Nuke").addCommand(mainMenu + 'Select Nodes/Select SelectionSet 03 Nodes', 'import transformNodesTools ; transformNodesTools.selectSelectionSet_Nodes(3)')

nuke.menu("Nuke").addCommand(mainMenu + 'Select Nodes/Select all nodes below the selected one', 'import transformNodesTools ; transformNodesTools.selectBelow()')
nuke.menu("Nuke").addCommand(mainMenu + 'Select Nodes/Select all nodes above the selected one', 'import transformNodesTools ; transformNodesTools.selectAbove()')
nuke.menu("Nuke").addCommand(mainMenu + 'Select Nodes/Select all nodes left of the selected one', 'import transformNodesTools ; transformNodesTools.selectLeft()')
nuke.menu("Nuke").addCommand(mainMenu + 'Select Nodes/Select all nodes right of the selected one', 'import transformNodesTools ; transformNodesTools.selectRight()')
nuke.menu("Nuke").addCommand(mainMenu + 'Select Nodes/Select all DOWNSTREAM', 'import transformNodesTools ; transformNodesTools.selectDownStream()')


nuke.menu("Nuke").addCommand(mainMenu + 'Arrange Nodes/Distribute Nodes evenly in X', 'import transformNodesTools ; transformNodesTools.distributeNodesEvenlyInX()')
nuke.menu("Nuke").addCommand(mainMenu + 'Arrange Nodes/Distribute Nodes evenly in Y', 'import transformNodesTools ; transformNodesTools.distributeNodesEvenlyInY()')
