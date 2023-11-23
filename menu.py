#Prasannakumar T Bhat
#This is the main menu.py file to load into nuke

#importing important modules
import os
import nuke
import nukescripts



# Submenu's
mainMenu = os.path.dirname(__file__).split('/')[-1]

p = nuke.menu("Nuke").addMenu(mainMenu)

p.addMenu('Help', index=0)
p.addMenu('NodeGraph', index=1)
p.addMenu('Utilities', index=2)
p.addMenu('Generate', index=3)


#help
nuke.menu('Nuke').addCommand(mainMenu + '/Help/GitHub', 'import pbSnippets ; pbSnippets.openWeb("https://github.com/pbhat99/pb.nuke/releases")', icon='pbicon.png')





#confirm full file loaded properly
nuke.tprint('pb tools Loaded!')
