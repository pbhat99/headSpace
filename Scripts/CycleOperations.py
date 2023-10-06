# Max van Leeuwen - maxvanleeuwen.com
# CycleOperations - 1.5
#
#
#
# The most-used knob of the selected node will cycle through its options, forwards or backwards (depending on the used keyboard shortcut).
# You won't have to open the properties box for the following nodes if you're only changing these knobs:
#
# Merge, ChannelMerge, and MergeMat will scroll through all merge operations. If you added items to the custom lists for these nodes, the nodes will only scroll through those!
# Switch will scroll through the node's inputs.
# Colorspace and OCIOColorspace will swap the in and out colourspaces.
# Shuffle will cycle the 'in' knob, and a label will display the current state.
# Keyer will cycle the 'operation' knob.
# FrameHold will increase or decrease the 'first_frame' knob value.
# Invert, Multiply, Blur, and Grade will cycle through the 'channels' knob.
# Log2Lin toggles log2lin and lin2log.
#
#
#
#
# Operation list example: ['minus', 'multiply', 'over', 'plus', 'screen']


C_Merge = []
C_ChannelMerge = []
C_MergeMat = []



#########################################


# TODO fix cycleoperations is other way around with valuemask, check blur or grade



import nuke




def Merge(n, cycle, forwards):

	try:

		# get knob
		k = n.knob('operation')


		# if custom list is used
		if len(cycle) > 0:

			# get knob value as str
			currOp = k.value()

			# check if current value is in cycle
			nextOp = ''

			if currOp in cycle:

				# get next or pevious item index (depending on forwards)
				index = cycle.index(currOp) + (1 if forwards else -1)

				# return to 0 if out of range
				if(index > (len(cycle)) - 1):
					index = 0

				# set new value
				nextOp = cycle[index]
			else:

				# reset to first in cycle
				nextOp = cycle[0]

			# set new value to knob
			n.knob("operation").setValue(nextOp)


		# if not, simply scroll through all options
		else:

			# current operation
			currOp = k.getValue()

			# operation count
			countOp = len(k.values())

			if forwards:

				# if last item in list, go to start
				if int(currOp) + 1 == countOp:
					k.setValue(0)

				else:
					k.setValue(int(currOp) + 1)

			else:

				if currOp == 0:
					k.setValue(countOp - 1)
				else:
					k.setValue(int(currOp) - 1)

	except:

		pass



def Switch(n, forwards):

	try:

		# get current value
		currWhich = n.knob('which').getValue()
		# get amount of inputs on Switch (-1, to match input index which starts counting at 0)
		maxWhich = n.inputs() - 1.0

		# make Switch nodes with only one input alternate between 1 and 0
		if(maxWhich == 0):
			maxWhich = 1

		# new value for Which on Switch
		newWhich = -1.0
		if forwards:

			newWhich = currWhich + 1.0
			if maxWhich < newWhich:
				newWhich = 0.0

		else:

			newWhich = currWhich - 1.0
			if newWhich < 0.0:
				newWhich = maxWhich

		n.knob('which').setValue(newWhich)

	except:

		pass



def OCIOColorSpace(n):

	try:

		# get knobs
		k1 = n.knob('in_colorspace')
		k2 = n.knob('out_colorspace')

		# get values
		inC = k1.value()
		outC = k2.value()

		# set inverse values
		k1.setValue(outC)
		k2.setValue(inC)

	except:

		pass



def Shuffle(n, forwards):

	try:

		# get knob
		try:
			k = n.knob('in')
		except:	
			k = n.knob('in1')

		# get current layer (str)
		currL = k.value()

		# get all existing layers
		listL = nuke.layers()

		# get index of current layer
		i = 0
		for eachL in listL:
			if eachL == currL:
				break
			i += 1

		# get new layer
		if forwards:

			if len(listL) == i + 1:
				newL = listL[0]
			else:
				newL = listL[i + 1]

		else:

			if i == 0:
				newL = listL[len(listL) - 1]
			else:
				newL = listL[i - 1]


		# set new layer
		k.setValue(newL)


		# set label
		giveLabel(n, 'in')

	except:

		pass



def FrameHold(n, forwards):

	try:

		# get knob
		k = n.knob('first_frame')

		# get current frame
		currF = k.getValue()

		# next value
		newF = currF + 1 if forwards else currF - 1

		# set new value
		k.setValue(newF)

	except:

		pass



def anyChannelKnob(n, knobName, forwards):

	try:

		# get knob
		k = n.knob(knobName)

		# get knob value (str)
		currL = k.value()

		# get all possible layers
		listL = nuke.layers()
		listL.insert(0, 'all')
		listL.insert(1, 'none')

		# get index of current layer
		i = 0
		for eachL in listL:
			if eachL == currL:
				break
			i += 1



		# get new layer
		if forwards:

			if len(listL) == i + 1:
				newL = listL[0]
			else:
				newL = listL[i + 1]

		else:

			if i == 0:
				newL = listL[len(listL) - 1]
			else:
				newL = listL[i - 1]


		# set new layer
		k.setValue(newL)
	

	except:

		pass



def anyListKnob(n, knobName, forwards):

	try:

		# get knob
		k = n.knob(knobName)

		# get knob value (int)
		currOp = k.getValue()

		# operation count
		countOp = len(k.values())


		# if forwards scrolling
		if forwards:

			# if last item in list, go to start
			if int(currOp) + 1 == countOp:
				k.setValue(0)

			else:
				# go forward one item
				k.setValue(int(currOp + 1))


		# scroll backwards
		else:

			# if at first item, go to end
			if currOp == 0:
				k.setValue(countOp - 1)

			# go back one item
			else:
				k.setValue(int(currOp - 1))

	except:

		pass



# make label show knob value (except if in valueMask list)
def giveLabel(n, knobName):

		# get label knob
		label = n.knob('label')

		# get current label text
		currLabel = label.getValue()

		# new label text
		labelText = '[value ' + knobName + ']'


		# check if the label is already present
		if not labelText in currLabel:

			# add original value and new line before new label text if there was a label already, else no new line
			if currLabel == '':
				label.setValue(labelText)
			else:
				label.setValue(currLabel + '\n' + labelText)



# cycle node (forwards or backwards)
def CycleOperations(forwards = True):

	# call function with cycle for each node
	for i in nuke.selectedNodes():

		# nodes with custom operation lists
		if i.Class() == 'Merge2':
			Merge(i, C_Merge, forwards)
		elif i.Class() == 'ChannelMerge':
			Merge(i, C_ChannelMerge, forwards)
		elif i.Class() == 'MergeMat':
			Merge(i, C_MergeMat, forwards)

		# scroll through switch inputs
		elif i.Class() == 'Switch':
			Switch(i, forwards)

		# swap colorspace in/outs
		elif i.Class() == 'Colorspace':
			i.knob('swap').execute()
		elif i.Class() == 'OCIOColorSpace':
			OCIOColorSpace(i)

		# cycle Shuffle
		elif i.Class() == 'Shuffle' or i.Class() == 'Shuffle2':
			Shuffle(i, forwards)

		# cycle Keyer
		elif i.Class() == 'Keyer':
			anyListKnob(i, 'operation', forwards)

		# up and down FrameHold
		elif i.Class() == 'FrameHold':
			FrameHold(i, forwards)

		elif i.Class() == 'Invert':
			anyChannelKnob(i, 'channel', forwards)
		elif i.Class() == 'Blur':
			anyChannelKnob(i, 'channel', forwards)
		elif i.Class() == 'Grade':
			anyChannelKnob(i, 'channel', forwards)
		elif i.Class() == 'Multiply':
			anyChannelKnob(i, 'channel', forwards)
		elif i.Class() == 'Log2Lin' or i.Class() == 'OCIOLogConvert':
			anyListKnob(i, 'operation', forwards)



# autostart (if not imported) - only goes forwards if called this way
if __name__ == "__main__":
	CycleOperations()