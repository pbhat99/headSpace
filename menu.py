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
nuke.menu('Nuke').addCommand('-{ pb }-/NodeGraph/Align Dots', "import AlignDots ; AlignDots.AlignDots()", 'Shift+.', shortcutContext=2)

#better backdrop & stickyNotes
nuke.menu('Nuke').addCommand('-{ pb }-/GrayAutoBackdrop', 'import GrayAutoBackdrop ; GrayAutoBackdrop.GrayAutoBackdrop()', 'alt+b', shortcutContext=2)

# pbSnippets 
nuke.menu('Nodes').addCommand('Other/StickyNote','import pbSnippets ; pbSnippets.pasteNote()','alt+n')
nuke.menu('Nuke').addCommand('-{ pb }-/GUI Disable','import pbSnippets ; pbSnippets.disableGUI()','shift+d')
nuke.menu("Nuke").addCommand('-{ pb }-/Change Label', 'import pbSnippets ; pbSnippets.nLabel()','n')
nuke.menu("Nuke").addCommand('-{ pb }-/Convert Gizmo','import pbSnippets ; pbSnippets.convertGizmosToGroups()','Ctrl+shift+g')
nuke.menu("Nuke").addCommand('-{ pb }-/NodeGraph/Mirror horizontally', 'import pbSnippets ; pbSnippets.MirrorNodes(nuke.selectedNodes(), direction="x", axis="last").start()')
nuke.menu("Nuke").addCommand('-{ pb }-/NodeGraph/Mirror vertically', 'import pbSnippets ; pbSnippets.MirrorNodes(nuke.selectedNodes(), direction="y", axis="last").start()')

#framehold to current frame as default
nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )", icon='FrameHold.png')


#W_smartAlign
nuke.menu('Nuke').addCommand('-{ pb }-/NodeGraph/Align Left', 'import W_smartAlign ; W_smartAlign.alignNodes("left")',"Alt+Shift+left", shortcutContext=2)
nuke.menu('Nuke').addCommand('-{ pb }-/NodeGraph/Align Right', 'import W_smartAlign ; W_smartAlign.alignNodes("right")',"Alt+Shift+right", shortcutContext=2)
nuke.menu('Nuke').addCommand('-{ pb }-/NodeGraph/Align Up',	'import W_smartAlign ; W_smartAlign.alignNodes("up")', "Alt+Shift+up", shortcutContext=2)
nuke.menu('Nuke').addCommand('-{ pb }-/NodeGraph/Align Down', 'import W_smartAlign ; W_smartAlign.alignNodes("down")', "Alt+Shift+down", shortcutContext=2)

#W_scaleTree
nuke.menu('Nuke').addCommand('-{ pb }-/NodeGraph/W_scaleTree', 'import W_scaleTree ; W_scaleTree.scaleTreeFloatingPanel()', 'alt+`')


#Cycle Operations
nuke.menu('Nuke').addCommand('-{ pb }-/Cycle Forwards', "import CycleOperations ; CycleOperations.CycleOperations()", "]", shortcutContext=2)
nuke.menu('Nuke').addCommand('-{ pb }-/Cycle Backwards', "import CycleOperations ; CycleOperations.CycleOperations(False)", "[", shortcutContext=2)


#channel hotbox
nuke.menu("Nuke").addCommand('-{ pb }-/Channel HotBox', 'import channel_hotbox ; channel_hotbox.start()', 'alt+q')


#reduce keyframes
nuke.menu('Animation').addCommand( '-{ pb }-/Reduce Keyframes', "import reduceKeyframes ; reduceKeyframes.doReduceKeyframes()" )

#AnimationMaker
nuke.menu('Animation').addCommand( '-{ pb }-/Animation Maker', 'import AnimationMaker ; AnimationMaker.showWindow()','',icon='ParticleBounce.png')


#confirm full file loaded properly
nuke.tprint('pb tools Loaded!')
