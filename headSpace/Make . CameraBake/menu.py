mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'Baked Camera','import cameraBake ; cameraBake.cameraBake()','', icon='pbicon.png')