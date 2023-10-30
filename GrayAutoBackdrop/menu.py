#better backdrop & stickyNotes
mainMenu = os.path.dirname(__file__).split('/')[-2]
nuke.menu('Nuke').addCommand(mainMenu + '/Utilities/GrayAutoBackdrop', 'import GrayAutoBackdrop ; GrayAutoBackdrop.GrayAutoBackdrop()', 'alt+b', shortcutContext=2, icon='pbicon.png')