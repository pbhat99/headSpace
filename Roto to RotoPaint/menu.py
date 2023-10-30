mainMenu = os.path.dirname(__file__).split('/')[-2]

nuke.menu("Nuke").addCommand(mainMenu + '/Generate/Convert Roto To Rotopaint', 'import RotoToRotopaint ; RotoToRotopaint.RotoToRotopaint()', icon='pbicon.png')

#Shortcut: SHIFT+P