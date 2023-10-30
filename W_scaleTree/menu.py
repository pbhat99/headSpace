#W_scaleTree
mainMenu = os.path.dirname(__file__).split('/')[-2]
nuke.menu('Nuke').addCommand(mainMenu + '/NodeGraph/-', '', '')
nuke.menu('Nuke').addCommand(mainMenu + '/NodeGraph/W_scaleTree', 'import W_scaleTree ; W_scaleTree.scaleTreeFloatingPanel()', 'alt+`', icon='pbicon.png')
nuke.menu('Nuke').addCommand(mainMenu + '/NodeGraph/-', '', '')