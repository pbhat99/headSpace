#Prasannakumar T Bhat
#This is the main menu.py file to load into nuke

#importing important modules
import os
import nuke
import nukescripts


def menuMaker():
	#makes menu names using folder names according to folder structure
	main = os.path.dirname(__file__).split('/')[-2]
	sub = os.path.dirname(__file__).split('/')[-1]
	sub = sub.split(' . ')
	if len(sub) > 1:
		sub = sub[:-1]
		sub = '/'.join(sub) + '/'
		menu = main + '/' + sub
	else:
		sub = ''
		menu = main + '/'
	return menu


# Submenu's
mainMenu = os.path.dirname(__file__).split('/')[-1]
p = nuke.menu("Nuke").addMenu(mainMenu)

p.addCommand( '-', '', '')
p.addMenu('Help', index=0)
p.addMenu('DAG', index=1)
p.addMenu('Utilities', index=2)
p.addMenu('Make', index=3)
p.addCommand( '-', '', '')


#help
nuke.menu('Nuke').addCommand(mainMenu + '/Help/GitHub', 'import pbSnippets ; pbSnippets.openWeb("https://github.com/pbhat99/pb.nuke/releases")', icon='pbicon.png')



# ctrl^
# shift+
# alt#

#confirm full file loaded properly
nuke.tprint('pb tools Loaded!')
