mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'Mirror horizontally', 'import mirrorNodes ; mirrorNodes.MirrorNodes(nuke.selectedNodes(), direction="x", axis="last").start()', icon='pbicon.png')
nuke.menu("Nuke").addCommand(mainMenu + 'Mirror vertically', 'import mirrorNodes ; mirrorNodes.MirrorNodes(nuke.selectedNodes(), direction="y", axis="last").start()', icon='pbicon.png')
nuke.menu('Nuke').addCommand(mainMenu + '-', '', '')
