#W_scaleTree
mainMenu = menuMaker()
nuke.menu('Nuke').addCommand(mainMenu + '-', '', '')
nuke.menu('Nuke').addCommand(mainMenu + 'W_scaleTree', 'import W_scaleTree ; W_scaleTree.scaleTreeFloatingPanel()', 'alt+`', icon='pbicon.png')
