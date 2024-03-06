mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'Camera Bake','import cameraBake ; cameraBake.cameraBake()','', icon='pbicon.png')