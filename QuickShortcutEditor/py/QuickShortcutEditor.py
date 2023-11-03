# QuickShortcutEditor v1.3 - Max van Leeuwen

# Change shortcuts in the accompanied 'Keyboard_Shortcuts.txt'-file.


import nuke
import os


# the text shown before any printed messages
QuickShortcutEditorText = "[QuickShortcutEditor v1.3] "


def loadUserprefs(userprefsPath):

	# create empty list for shortcuts
	scList = []

	# check if the specified userprefspath exists
	if (os.path.isfile(userprefsPath)):

		# if it does, load the text line by line to a list
		with open(userprefsPath) as f:
			lines = f.readlines()


		# iterate through each line
		i = 0
		for line in lines:

			# if the line does not contain '#' in the first character
			if not ('#' in line[0]):

				# replace any newline characters in the line
				line = line.replace('\n', '')

				# split by tabs
				columns = line.split('\t')

				# make empty list of shortcut values for this line
				scEntry = []

				# for each column split by tabs
				for column in columns:

					# if the column is not empty
					if column != '' and column != ' ':

						# add to entry list
						scEntry.append(column)

				# get the amount of values enteres
				args = len(scEntry)
				if (args > 3):
					# more values than expected
					print (QuickShortcutEditorText + "Error: Could not read line " + str(i) + " in Keyboard_Shortcuts.txt")
				elif (args == 3):
					# a shortcut context has been given as well, add entry shortcut list
					scList.append(scEntry)
				elif (args == 2):
					# no shortcutc context has been given, add entry to shortcut list and add context '0'
					scEntry.insert(2, '0')
					scList.append(scEntry)
				elif (args < 2):
					# not enough arguments, ignore
					pass

			# count iterations
			i += 1

	else:
		# file does not exist
		print (QuickShortcutEditorText + "Error: File does not exist")

	# return list
	return scList


def assign(scPath, scKey, scContext):

	try:
		
		# get the first part of the path for the menu type
		scMenutype = scPath.split('/')[0]

		# get everything else from the item path
		scPathAftertype = scPath.replace(scMenutype, '')[1:]

		# get nuke menu defined from type
		menu = nuke.menu(scMenutype)
		# find the item from scPathAdterType and look up its command
		command = menu.findItem(scPathAftertype).script()

		# add the command to the menu - if the nuke version is >= 9, use shortcut context
		if nuke.env['NukeVersionMajor'] < 9:
			menu.addCommand(scPathAftertype, command, scKey)
		else:
			menu.addCommand(scPathAftertype, command, scKey, shortcutContext=int(scContext))
	except:
		# on error
		print (QuickShortcutEditorText + "Error: Could not assign shortcut to: " + scPath)


def assignfromFile(userprefsPath):

	# make a shortcut list by loading the text file from userprefsPath
	scList = loadUserprefs(userprefsPath)

	# for each item in the list, assign it using the assign() function
	i = 0
	for sc in scList:
		assign(scList[i][0], scList[i][1].replace(' ', ''), scList[i][2])
		i += 1