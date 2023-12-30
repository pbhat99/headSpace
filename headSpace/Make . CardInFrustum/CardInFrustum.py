# Max van Leeuwen - maxvanleeuwen.com
# CardInFrustum - 1.1
#
# Make a card that is oriented towards the selected camera node, and fit it in its frustum. Can be expression-linked, or placed on one frame.


import nuke


def CardInFrustum():

	# text to display when no camera is selected
	NoCamSelected = 'Select a camera node to create a frustum plane for!'

	# cam variable
	cam = None
	try:

		# get the selected node
		sel = nuke.selectedNode()

		# check if the node is a camera node
		if sel.Class().startswith('Camera'):
			cam = sel
		else:
			nuke.message(NoCamSelected)

	except:
		nuke.message(NoCamSelected)


	# if the selected node is a camera
	if cam is not None:

		# ask if the card should be linked to the camera frustum or if it should be set to the position on the current frame
		link = nuke.ask('Should the card be linked to ' + cam.name() + ' with an expression?\nElse, only this frame will be matched.')

		# make card
		ca = nuke.nodes.Card2()
		
		# set card node xpos and ypos to something near the camera
		ca.setXpos(cam.xpos() + 80)
		ca.setYpos(cam.ypos() + 80)

		# set the z of the card to 1, and set the useMatrix to enabled
		ca['z'].setValue(1)
		ca['useMatrix'].setValue(1)

		# if link is True
		if(link):

			# set the focal length, aperture and matrix to that of the camera
			ca['lens_in_focal'].setExpression(cam.name() + '.focal')
			ca['lens_in_haperture'].setExpression(cam.name() + '.haperture')
			ca['matrix'].setExpression(cam.name() + '.matrix')

		else:

			ca['lens_in_focal'].setValue(cam['focal'].getValue())
			ca['lens_in_haperture'].setValue(cam['haperture'].getValue())
			ca['matrix'].setValue(cam['matrix'].getValue())


# autostart (if not imported)
if __name__ == "__main__":
	CardInFrustum()