# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
# Edit by Max van Leeuwen - maxvanleeuwen.com - 1.3

# PREFERENCES FOR DEFAULT SETTINGS:


# sticky note default label size
defaultStickyLabelSize = '50'

# sticky note default color
defaultStickyColor = 3435954431

# change colors of the backdrops that are within the newly created one
defaultUpdateBackdrops = True

# color for backdrop (stacked backdrops will get darker)
startingColor = 1179010815

# backdrop colors to never change (photoshop breakout layers)
ignoreColors = [2829621248, 1751668736]

# backdrop boundaries scaling
bdSize = .5


############################################






import nuke, random
import colorsys




# make every stacked backdrop slightly darker
def darker(levels):

	newColor = startingColor

	for i in range( int( abs(levels) ) ):
		RGB = [(0xFF & newColor >>  i) / 255.0 for i in [24,16,8]]
		HSV = colorsys.rgb_to_hsv(RGB[0],RGB[1],RGB[2])

		newHSV = [HSV[0], HSV[1], HSV[2] * .85]
		newRGB = colorsys.hsv_to_rgb(newHSV[0],newHSV[1],newHSV[2])

		newColor = int('%02x%02x%02x%02x' % (round(newRGB[0]*255),round(newRGB[1]*255),round(newRGB[2]*255),255),16)

	return newColor




def nodeIsInside(node, backdropNode):

	"""Returns true if node geometry is inside backdropNode otherwise returns false"""

	topLeftNode = [node.xpos(), node.ypos()]
	topLeftBackDrop = [backdropNode.xpos(), backdropNode.ypos()]
	bottomRightNode = [node.xpos() + node.screenWidth(), node.ypos() + node.screenHeight()]
	bottomRightBackdrop = [backdropNode.xpos() + backdropNode.screenWidth(), backdropNode.ypos() + backdropNode.screenHeight()]

	topLeft = ( topLeftNode[0] >= topLeftBackDrop[0] ) and ( topLeftNode[1] >= topLeftBackDrop[1] )
	bottomRight = ( bottomRightNode[0] <= bottomRightBackdrop[0] ) and ( bottomRightNode[1] <= bottomRightBackdrop[1] )

	return topLeft and bottomRight




# function can be called with custom default variables
def GrayAutoBackdrop():


	global defaultStickyLabelSize
	global defaultStickyColor
	global defaultUpdateBackdrops



	bdUpdateBooleantext = 'update included backdrops?'


	'''
	Automatically puts a backdrop behind the selected nodes.

	The backdrop will be just big enough to fit all the select nodes in, with room
	at the top for some text in a large font.
	'''


	# check if nodes are selected
	selNodes = nuke.selectedNodes()
	if selNodes:

		# panel
		p = nuke.Panel('backdrop')
		p.addSingleLineInput('label', '')
		p.addBooleanCheckBox(bdUpdateBooleantext, defaultUpdateBackdrops)

		panelObj = p.show()


		if panelObj:

			# calculate bounds for the backdrop node.
			bdX = min([node.xpos() for node in selNodes])
			bdY = min([node.ypos() for node in selNodes])
			bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
			bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY


			# bigger boundaries if node area is bigger
			boundsMult = 10 + (bdW + bdH) * (bdSize/100)
			zOrder = 0

			defaultUpdateBackdrops = p.value(bdUpdateBooleantext)
			noBackdropNodes = False
			
			if defaultUpdateBackdrops:

				selectedBackdropNodes = nuke.selectedNodes("BackdropNode")

				# if there are backdropNodes selected, put the new one at the lowest level and all others at their own level + 1
				if len(selectedBackdropNodes):

					# placeholders
					lowest = 99999
					offs = 0

					for sBD in selectedBackdropNodes:

						currVal = sBD['z_order'].value()
						lowest = min(lowest, currVal)

					# all backdrops must be => 0
					if lowest < 0:
						offs = abs(lowest)
						lowest = 0

					for sBD in selectedBackdropNodes:

						currVal = sBD['z_order'].value()

						newZ = currVal + 1 + offs
						sBD['z_order'].setValue(newZ)

						if not sBD['tile_color'].value() in ignoreColors:
							sBD['tile_color'].setValue(darker(newZ))

					zOrder = lowest


				else:

					noBackdropNodes = True



			if (not defaultUpdateBackdrops) or noBackdropNodes:

				# else (no backdrop in selection) find the nearest backdrop if exists and set the new one in front of it
				nonSelectedBackdropNodes = nuke.allNodes("BackdropNode")

				for nonBackdrop in selNodes:

					for backdrop in nonSelectedBackdropNodes:

						if nodeIsInside( nonBackdrop, backdrop ):

							zOrder = max(zOrder, backdrop.knob("z_order").value() + 1 )



			# Expand the bounds to leave a border, relative to zoom size. Elements are offsets for left, top, right and bottom edges respectively. Extra top height if larger label.
			left, top, right, bottom = (-10 * boundsMult, -80 - 10 * boundsMult, 10 * boundsMult, 10 * boundsMult)
			bdX += left
			bdY += top
			bdW += (right - left)
			bdH += (bottom - top)


			labelstr = p.value('label')

			n = nuke.nodes.BackdropNode(xpos = bdX,
										bdwidth = bdW,
										ypos = bdY,
										bdheight = bdH,
										note_font_size = 100,
										tile_color = darker(zOrder if defaultUpdateBackdrops else 0),
										z_order = zOrder if defaultUpdateBackdrops else 0,
										label = labelstr)

			# revert to previous selection + this backdrop
			n['selected'].setValue(True)
			for node in selNodes:
				node['selected'].setValue(True)

			return n

		else:
			pass



	# if no nodes are selected, make sticky note
	else:

		# panel
		p = nuke.Panel('stickynote')
		p.addSingleLineInput('label', '')
		p.addSingleLineInput('label size', defaultStickyLabelSize)
		p.addButton('cancel')
		p.addButton('done')
		p.addButton('color')

		# show panel
		panelObj = p.show()


		# if user did not cancel panel or leave label empty
		if panelObj:

			# get color form different panel, because the RGBChip in nuke's panel is broken
			if(panelObj == 2):
				colObj = nuke.getColor(defaultStickyColor)
				if colObj:
					defaultStickyColor = colObj

			# try to get and set label size
			try:
				l = int(p.value('label size'))
				defaultStickyLabelSize = l
			except:
				pass


			# make stickynote, show panel if the label was empty (the user might want to type multiline text)
			n = nuke.createNode("StickyNote", inpanel=(p.value('label') == ''))
			n['note_font_size'].setValue(defaultStickyLabelSize)
			n['label'].setValue(p.value('label'))
			n['tile_color'].setValue(defaultStickyColor)

			n.setXpos(n.xpos() - round(n.screenWidth()/2))
			n.setYpos(n.ypos() + round(n.screenHeight()/2))




# autostart (if not imported)
if __name__ == "__main__":
	GrayAutoBackdrop()