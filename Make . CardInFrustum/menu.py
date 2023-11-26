mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'Card In Frustum','import CardInFrustum ; CardInFrustum.CardInFrustum()','', icon='pbicon.png')