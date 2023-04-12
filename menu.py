#Prasannakumar T Bhat
#This is the main menu.py file to load into nuke

#Let me confirm loading of this file in nuke terminal
nuke.tprint('Loading Custom Tools by Prasannakumar T Bhat')

#importing important modules
import os
import nuke

import W_hotbox
import W_hotboxManager
import KnobScripter


#my knobdefaults & snippets
import pbKnobDefaults


#Import all nodes from another script
#nuke.loadToolset("/home/user/Templates/script.nk")

# comma tool
nuke.menu("Nodes").addCommand('Other/Comma','import comma ; comma.makeComma()',',',icon='Comma.png',index=6)

# dot create and align tool
nuke.menu('Nuke').addCommand('-{ pb }-/Align Dots', "import AlignDots ; AlignDots.AlignDots()", 'Shift+.', shortcutContext=2)

#better backdrop & stickyNotes
nuke.menu('Nuke').addCommand('-{ pb }-/GrayAutoBackdrop', 'import GrayAutoBackdrop ; GrayAutoBackdrop.GrayAutoBackdrop()', 'alt+b', shortcutContext=2)

# pbSnippets 
nuke.menu('Nuke').addCommand('-{ pb }-/GUI Disable','import pbSnippets ; pbSnippets.disableGUI()','shift+d')
nuke.menu('Nodes').addCommand('Other/StickyNote','import pbSnippets ; pbSnippets.pasteNote()','alt+n')
nuke.menu("Nuke").addCommand("Edit/Node/Label", "import pbSnippets ; pbSnippets.nLabel()","n")

#framehold to current frame as default
nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )", icon='FrameHold.png')




#confirm full file loaded properly
nuke.tprint('pb tools Loaded!')
