
import pbKnobDefaults
#import pbAutoLabel


# pbSnippets 
nuke.menu('Nodes').addCommand('Other/StickyNote','import pbSnippets ; pbSnippets.pasteNote()','alt+n', icon='pbicon.png')
#nuke.menu('Nuke').addCommand(mainMenu + '/Utilities/Disable in GUI','import pbSnippets ; pbSnippets.disableGUI()','shift+d', icon='pbicon.png')
#nuke.menu("Nuke").addCommand(mainMenu + '/Utilities/Change Label', 'nuke.load("pbSnippets"), nLabel()','n', icon='pbicon.png')
nuke.menu("Nuke").menu(mainMenu).addSeparator()