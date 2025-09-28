
mainMenu = menuMaker()
nuke.menu("Nuke").addCommand(mainMenu + 'superRead', 'nuke.load("superRead") , superRead()', 'e', shortcutContext=2, icon = 'pbIcon.png')
