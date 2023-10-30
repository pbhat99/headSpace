#Prasannakumar T Bhat
#This is the main menu.py file to load into nuke

#importing important modules
import os
import nuke
import nukescripts



#my knobdefaults & snippets

#pbtoolbar = nuke.menu("Nuke").addMenu(mainMenu + '')

import pbKnobDefaults
import pbAutoLabel

# Submenu's
mainMenu = os.path.dirname(__file__).split('/')[-1]

p = nuke.menu("Nuke").addMenu(mainMenu)

p.addMenu('Help', index=0)
p.addMenu('NodeGraph', index=1)
p.addMenu('Utilities', index=2)
p.addMenu('Generate', index=3)


#help
nuke.menu('Nuke').addCommand(mainMenu + '/Help/GitHub', 'import pbSnippets ; pbSnippets.openWeb("https://github.com/pbhat99/pb.nuke/releases")', icon='pbicon.png')


# pbSnippets 
nuke.menu('Nodes').addCommand('Other/StickyNote','import pbSnippets ; pbSnippets.pasteNote()','alt+n', icon='pbicon.png')
nuke.menu('Nuke').addCommand(mainMenu + '/Utilities/Disable in GUI','import pbSnippets ; pbSnippets.disableGUI()','shift+d', icon='pbicon.png')
#nuke.menu("Nuke").addCommand(mainMenu + '/Utilities/Change Label', 'nuke.load("pbSnippets"), nLabel()','n', icon='pbicon.png')
nuke.menu("Nuke").menu(mainMenu).addSeparator()





#confirm full file loaded properly
nuke.tprint('pb tools Loaded!')
