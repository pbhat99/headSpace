mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'Cards along Camera Path','import cardsFromCamPath ; cardsFromCamPath.cardsFromCamPath()','', icon='pbicon.png')
