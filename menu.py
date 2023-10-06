#Prasannakumar T Bhat
#This is the main menu.py file to load into nuke

#importing important modules
import os
import nuke
import nukescripts



#my knobdefaults & snippets

pbtoolbar = nuke.menu("Nuke").addMenu('-{ pb }-')

import pbKnobDefaults

# Submenu's
import os
submenu = os.path.dirname(__file__).split('/')[-1]

p = nuke.menu("Nuke").addMenu('-{ pb }-')

p.addMenu('Help', index=0)
p.addMenu('NodeGraph', index=1)
p.addMenu('Utilities', index=2)
p.addMenu('Convert', index=3)


#help
nuke.menu('Nuke').addCommand('-{ pb }-/Help/GitHub', 'import pbSnippets ; pbSnippets.openWeb("https://github.com/pbhat99/pb.nuke/releases")', icon='pbicon.png')


# pbSnippets 
nuke.menu('Nodes').addCommand('Other/StickyNote','import pbSnippets ; pbSnippets.pasteNote()','alt+n', icon='pbicon.png')
nuke.menu('Nuke').addCommand('-{ pb }-/Utilities/Disable in GUI','import pbSnippets ; pbSnippets.disableGUI()','shift+d', icon='pbicon.png')
#nuke.menu("Nuke").addCommand('-{ pb }-/Utilities/Change Label', 'nuke.load("pbSnippets"), nLabel()','n', icon='pbicon.png')
nuke.menu("Nuke").menu('-{ pb }-').addSeparator()

#Cycle Operations
nuke.menu('Nuke').addCommand('-{ pb }-/Cycle Operation/Forwards', "import CycleOperations ; CycleOperations.CycleOperations()", "]", shortcutContext=2, icon='pbicon.png')
nuke.menu('Nuke').addCommand('-{ pb }-/Cycle Operation/Backwards', "import CycleOperations ; CycleOperations.CycleOperations(False)", "[", shortcutContext=2, icon='pbicon.png')



#framehold to current frame as default
nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )", icon='FrameHold.png')



#confirm full file loaded properly
nuke.tprint('pb tools Loaded!')
