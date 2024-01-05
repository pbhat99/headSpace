# http://www.nukepedia.com/python/nodegraph/transformnodestools
# Contributor: Vincent Langer
# Website: www.vincentlanger.com
# A collection of simple node UI transform tools. Great for very large scripts. Lets you easily move/rotate/scale/mirror nodes with keyboard shortcuts.


import sys, os, re
import nuke, nukescripts


def getBoundingBoxOfSelNodes():

	selNodes = nuke.selectedNodes()
	
	if (len(selNodes) != 0) :
		minX = selNodes[0].xpos()
		maxX = selNodes[0].xpos()
		minY = selNodes[0].ypos()
		maxY = selNodes[0].ypos()
		
		for node in selNodes:
			if node.Class() == 'BackdropNode':
				if (node.xpos() + node['bdwidth'].value()) >maxX:
					maxX = (node.xpos() + node['bdwidth'].value())
				if node.xpos()<minX:
					minX = node.xpos()
			
				if (node.ypos() + node['bdheight'].value()) >maxY:
					maxY = (node.ypos() + node['bdheight'].value())
				if node.ypos()<minY:
					minY = node.ypos()
			
			else:
				if node.xpos()>maxX:
					maxX = node.xpos()
				if node.xpos()<minX:
					minX = node.xpos()
			
				if node.ypos()>maxY:
					maxY = node.ypos()
				if node.ypos()<minY:
					minY = node.ypos()
		
		return [minX, maxX, minY, maxY]
	else:
		return [0,0,0,0]
			
def nudgeNodes_up():
	sel = nuke.selectedNodes()
	for node in sel:
		node.setXYpos(node.xpos(),node.ypos()-200)
		
def nudgeNodes_down():
	sel = nuke.selectedNodes()
	for node in sel:
		node.setXYpos(node.xpos(),node.ypos()+200)
		
def nudgeNodes_right():
	sel = nuke.selectedNodes()
	for node in sel:
		node.setXYpos(node.xpos()+200,node.ypos())
		
def nudgeNodes_left():
	sel = nuke.selectedNodes()
	for node in sel:
		node.setXYpos(node.xpos()-200,node.ypos())
			
def nudgeNodes_up_more():
	sel = nuke.selectedNodes()
	for node in sel:
		node.setXYpos(node.xpos(),node.ypos()-800)
		
def nudgeNodes_down_more():
	sel = nuke.selectedNodes()
	for node in sel:
		node.setXYpos(node.xpos(),node.ypos()+800)
		
def nudgeNodes_right_more():
	sel = nuke.selectedNodes()
	for node in sel:
		node.setXYpos(node.xpos()+800,node.ypos())
		
def nudgeNodes_left_more():
	sel = nuke.selectedNodes()
	for node in sel:
		node.setXYpos(node.xpos()-800,node.ypos())

def deleteBackDropsInSelection():
	sel = nuke.selectedNodes('BackdropNode')
	for bdNode in sel:
		nuke.delete(bdNode)

def scaleNodePositionsInXandY():
	if nuke.exists('PIVOT_DOT'):
		xPivot = nuke.toNode('PIVOT_DOT').xpos()
		yPivot = nuke.toNode('PIVOT_DOT').ypos()
	else:
		bounds = getBoundingBoxOfSelNodes()
		xPivot = bounds[0]+((bounds[1]-bounds[0])/2)
		yPivot = bounds[2]+((bounds[3]-bounds[2])/2)

	selNodes = nuke.selectedNodes()

	for node in selNodes:
		node.setXYpos(int(((node.xpos() - xPivot ) *0.9)+xPivot) , int(((node.ypos() - yPivot ) *0.9)+yPivot))
		if node.Class() == 'BackdropNode':
			node['bdwidth'].setValue(node['bdwidth'].value() * 0.9)
			node['bdheight'].setValue(node['bdheight'].value() * 0.9)

def scaleNodePositionsInXonly():
	if nuke.exists('PIVOT_DOT'):
		xPivot = nuke.toNode('PIVOT_DOT').xpos()
		yPivot = nuke.toNode('PIVOT_DOT').ypos()
	else:
		bounds = getBoundingBoxOfSelNodes()
		xPivot = bounds[0]+((bounds[1]-bounds[0])/2)
		

	selNodes = nuke.selectedNodes()

	for node in selNodes:
		node.setXpos(int(((node.xpos() - xPivot ) *0.9)+xPivot) )
		if node.Class() == 'BackdropNode':
			node['bdwidth'].setValue(node['bdwidth'].value() * 0.9)
	
def scaleNodePositionsInYonly():
	if nuke.exists('PIVOT_DOT'):
		xPivot = nuke.toNode('PIVOT_DOT').xpos()
		yPivot = nuke.toNode('PIVOT_DOT').ypos()
	else:
		bounds = getBoundingBoxOfSelNodes()
		yPivot = bounds[2]+((bounds[3]-bounds[2])/2)

	selNodes = nuke.selectedNodes()

	for node in selNodes:
		node.setYpos(int(((node.ypos() - yPivot ) *0.9)+yPivot))
		if node.Class() == 'BackdropNode':
			node['bdheight'].setValue(node['bdheight'].value() * 0.9)
		
def scaleNodePositionsOutXandY():
	if nuke.exists('PIVOT_DOT'):
		xPivot = nuke.toNode('PIVOT_DOT').xpos()
		yPivot = nuke.toNode('PIVOT_DOT').ypos()
	else:
		bounds = getBoundingBoxOfSelNodes()

		xPivot = bounds[0]+((bounds[1]-bounds[0])/2)
		yPivot = bounds[2]+((bounds[3]-bounds[2])/2)

	selNodes = nuke.selectedNodes()

	for node in selNodes:
		node.setXYpos(int(((node.xpos() - xPivot ) *1.1)+xPivot) , int(((node.ypos() - yPivot ) *1.1)+yPivot))
		if node.Class() == 'BackdropNode':
			node['bdwidth'].setValue(node['bdwidth'].value() * 1.1)
			node['bdheight'].setValue(node['bdheight'].value() * 1.1)

def scaleNodePositionsOutXonly():
	if nuke.exists('PIVOT_DOT'):
		xPivot = nuke.toNode('PIVOT_DOT').xpos()
		yPivot = nuke.toNode('PIVOT_DOT').ypos()
	else:
		bounds = getBoundingBoxOfSelNodes()
		xPivot = bounds[0]+((bounds[1]-bounds[0])/2)

	selNodes = nuke.selectedNodes()

	for node in selNodes:
		node.setXpos(int(((node.xpos() - xPivot ) *1.1)+xPivot))
		if node.Class() == 'BackdropNode':
			node['bdwidth'].setValue(node['bdwidth'].value() * 1.1)

def scaleNodePositionsOutYonly():
	if nuke.exists('PIVOT_DOT'):
		xPivot = nuke.toNode('PIVOT_DOT').xpos()
		yPivot = nuke.toNode('PIVOT_DOT').ypos()
	else:
		bounds = getBoundingBoxOfSelNodes()

		yPivot = bounds[2]+((bounds[3]-bounds[2])/2)

	selNodes = nuke.selectedNodes()

	for node in selNodes:
		node.setYpos(int(((node.ypos() - yPivot ) *1.1)+yPivot))
		if node.Class() == 'BackdropNode':
			node['bdheight'].setValue(node['bdheight'].value() * 1.1)
			
def rotateNodes90DegreesCW():
	if nuke.exists('PIVOT_DOT'):
		xPivot = nuke.toNode('PIVOT_DOT').xpos()
		yPivot = nuke.toNode('PIVOT_DOT').ypos()
	else:
		bounds = getBoundingBoxOfSelNodes()

		xPivot = bounds[0]+((bounds[1]-bounds[0])/2)
		yPivot = bounds[2]+((bounds[3]-bounds[2])/2)

	selNodes = nuke.selectedNodes()

	for node in selNodes:
		if node.Class() == 'BackdropNode':
		
			#x = (node.ypos() + (node['bdheight'].value()/2) - yPivot ) + xPivot - (node['bdwidth'].value()/2)
			#y = ((node.xpos() + (node['bdwidth'].value()/2) - xPivot )*-1) + yPivot - (node['bdheight'].value()/2)
			#node.setXYpos(int( x ) , int( y ) )
			if node['bdheight'].value() > node['bdwidth'].value():
				x = (node.ypos() + (node['bdheight'].value()/2) - yPivot ) + xPivot - (node['bdwidth'].value()/2) - (( node['bdheight'].value() - node['bdwidth'].value() ) / 2 )
				y = ((node.xpos() + (node['bdwidth'].value()/2) - xPivot )*-1) + yPivot - (node['bdheight'].value()/2) + (( node['bdheight'].value() - node['bdwidth'].value() ) / 2 )
			else:
				x = (node.ypos() + (node['bdheight'].value()/2) - yPivot ) + xPivot - (node['bdwidth'].value()/2) + (( node['bdwidth'].value() - node['bdheight'].value() ) / 2 )
				y = ((node.xpos() + (node['bdwidth'].value()/2) - xPivot )*-1) + yPivot - (node['bdheight'].value()/2) - (( node['bdwidth'].value() - node['bdheight'].value() ) / 2 )
				
			node.setXYpos(int( x ) , int( y ) )
			oldWidthValue = node['bdwidth'].value()
			node['bdwidth'].setValue(node['bdheight'].value())
			node['bdheight'].setValue(oldWidthValue)
			
		else:
			x = (node.ypos()-yPivot) + xPivot
			y = ((node.xpos()-xPivot)*-1) +yPivot
			node.setXYpos(int( x ) , int( y ) )

def rotateNodes90DegreesCCW():
	if nuke.exists('PIVOT_DOT'):
		xPivot = nuke.toNode('PIVOT_DOT').xpos()
		yPivot = nuke.toNode('PIVOT_DOT').ypos()
	else:
		bounds = getBoundingBoxOfSelNodes()

		xPivot = bounds[0]+((bounds[1]-bounds[0])/2)
		yPivot = bounds[2]+((bounds[3]-bounds[2])/2)

	selNodes = nuke.selectedNodes()

	for node in selNodes:
		if node.Class() == 'BackdropNode':
		
			if node['bdheight'].value() > node['bdwidth'].value():
				x = ((node.ypos() + (node['bdheight'].value()/2) - yPivot )*-1) + xPivot - (node['bdwidth'].value()/2) - (( node['bdheight'].value() - node['bdwidth'].value() ) / 2 )
				y = ((node.xpos() + (node['bdwidth'].value()/2) - xPivot )) + yPivot - (node['bdheight'].value()/2) + (( node['bdheight'].value() - node['bdwidth'].value() ) / 2 )
			else:
				x = ((node.ypos() + (node['bdheight'].value()/2) - yPivot )*-1) + xPivot - (node['bdwidth'].value()/2) + (( node['bdwidth'].value() - node['bdheight'].value() ) / 2 )
				y = ((node.xpos() + (node['bdwidth'].value()/2) - xPivot )) + yPivot - (node['bdheight'].value()/2) - (( node['bdwidth'].value() - node['bdheight'].value() ) / 2 )
				
			node.setXYpos(int( x ) , int( y ) )
			oldWidthValue = node['bdwidth'].value()
			node['bdwidth'].setValue(node['bdheight'].value())
			node['bdheight'].setValue(oldWidthValue)
			
		else:
			x = ((node.ypos()-yPivot)*-1) + xPivot
			y = (node.xpos()-xPivot) +yPivot
			node.setXYpos(int( x ) , int( y ) )	

def mirrorX():
	if nuke.exists('PIVOT_DOT'):
		xPivot = nuke.toNode('PIVOT_DOT').xpos()
	else:
		bounds = getBoundingBoxOfSelNodes()
		xPivot = bounds[0]+((bounds[1]-bounds[0])/2)

	selNodes = nuke.selectedNodes()
	for node in selNodes:
		if node.Class() == 'BackdropNode':

			node.setXpos(int( (xPivot - node.xpos()) + xPivot - node['bdwidth'].value()) )

		else:
			node.setXpos(int( (xPivot - node.xpos()) + xPivot ) )		

def mirrorY():
	if nuke.exists('PIVOT_DOT'):
		yPivot = nuke.toNode('PIVOT_DOT').ypos()
	else:
		bounds = getBoundingBoxOfSelNodes()
		yPivot = bounds[2]+((bounds[3]-bounds[2])/2)

	selNodes = nuke.selectedNodes()

	for node in selNodes:
		if node.Class() == 'BackdropNode':
			node.setYpos(int( (yPivot - node.ypos()) + yPivot ) - node['bdheight'].value() )	
		else:
			node.setYpos(int( (yPivot - node.ypos()) + yPivot ) )		
			
def createPivotDot():
	
	for selNode in nuke.selectedNodes():
		selNode.setSelected(0)
	
	if nuke.exists('PIVOT_DOT'):
		nuke.delete(nuke.toNode('PIVOT_DOT'))

	pivotDot = nuke.createNode("Dot", inpanel=False)
	pivotDot.setName('PIVOT_DOT')
	pivotDot['label'].setValue('PIVOT_DOT')
	pivotDot['note_font_size'].setValue(40)

def deletePivotDot():	
	if nuke.exists('PIVOT_DOT'):
		nuke.delete(nuke.toNode('PIVOT_DOT'))

def distributeNodesEvenlyInX():

	bounds = getBoundingBoxOfSelNodes()

	selNodes = nuke.selectedNodes()
	sortList= []
	for node in selNodes:
		sortList.append([node.xpos() , node])
	sortList.sort()

	stepSize = int((bounds[1] - bounds[0]) / (len(sortList)-1))
	for i in range(len(sortList)):
		sortList[i][1].setXpos(bounds[0] + i * stepSize)

def distributeNodesEvenlyInY():

	bounds = getBoundingBoxOfSelNodes()

	selNodes = nuke.selectedNodes()
	sortList= []
	for node in selNodes:
		sortList.append([node.ypos() , node])
	sortList.sort()

	stepSize = int((bounds[3] - bounds[2]) / (len(sortList)-1))
	for i in range(len(sortList)):
		sortList[i][1].setYpos(bounds[2] + i * stepSize)

def selectBelow():
	if len(nuke.selectedNodes()) != 0:
		selNode = nuke.selectedNodes()[0]

	allNodes = nuke.allNodes()

	for node in allNodes:
		if node.ypos() >= selNode.ypos() :
			node.setSelected(1)
			
def selectAbove():
	if len(nuke.selectedNodes()) != 0:
		selNode = nuke.selectedNodes()[0]

	allNodes = nuke.allNodes()

	for node in allNodes:
		if node.ypos() <= selNode.ypos() :
			node.setSelected(1)
			
def selectLeft():
	if len(nuke.selectedNodes()) != 0:
		selNode = nuke.selectedNodes()[0]

	allNodes = nuke.allNodes()

	for node in allNodes:
		if node.xpos() <= selNode.xpos() :
			node.setSelected(1)
			
def selectRight():
	if len(nuke.selectedNodes()) != 0:
		selNode = nuke.selectedNodes()[0]

	allNodes = nuke.allNodes()

	for node in allNodes:
		if node.xpos() >= selNode.xpos() :
			node.setSelected(1)	

	
def selectDepent(mynode):
	dependentNodes = set()
	if mynode.dependent() != [] :
		for dep in mynode.dependent():
			dependentNodes |= set([dep])
			dependentNodes |= selectDepent(dep)
	return dependentNodes

def selectDownStream():
	sel = nuke.selectedNodes()
	dependentNodes = set()
	for node in sel[:]:
		dependentNodes |= selectDepent(node)
	for each in list(dependentNodes):
		each.setSelected(1)


def addSelectionToSelectionSet(number):
	sel = nuke.selectedNodes()
	
	for node in sel:
		if 'SelectionSetGroup' not in node.knobs().keys():
			node.addKnob(nuke.Tab_Knob('SelSetInfo'))
			node.addKnob( nuke.Int_Knob('SelectionSetGroup') )
		node['SelectionSetGroup'].setValue(number)
		
		
def selectSelectionSet_Nodes(number):
	allNodes = nuke.allNodes()
	for node in allNodes:
		if 'SelectionSetGroup' in node.knobs().keys():
			if node['SelectionSetGroup'].value() == number:
				node.setSelected(1)
			else:
				node.setSelected(0)
		else:
			node.setSelected(0)

