mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'superRead', 'import superRead ; superRead.superRead()', 'e', shortcutContext=2, icon = 'pbIcon.png')