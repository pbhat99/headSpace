#better backdrop & stickyNotes
mainMenu = menuMaker()
nuke.menu('Nuke').addCommand(mainMenu + 'GrayAutoBackdrop', 'import GrayAutoBackdrop ; GrayAutoBackdrop.GrayAutoBackdrop()', 'alt+b', shortcutContext=2, icon='pbicon.png')
