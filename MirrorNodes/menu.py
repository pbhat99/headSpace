mainMenu = os.path.dirname(__file__).split('/')[-2]

nuke.menu("Nuke").addCommand(mainMenu + '/NodeGraph/Mirror horizontally', 'import mirrorNodes ; mirrorNodes.MirrorNodes(nuke.selectedNodes(), direction="x", axis="last").start()', icon='pbicon.png')
nuke.menu("Nuke").addCommand(mainMenu + '/NodeGraph/Mirror vertically', 'import mirrorNodes ; mirrorNodes.MirrorNodes(nuke.selectedNodes(), direction="y", axis="last").start()', icon='pbicon.png')
nuke.menu("Nuke").menu(mainMenu + '/NodeGraph').addSeparator()