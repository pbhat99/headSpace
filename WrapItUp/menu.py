#WrapItUp - pack nuke script with dependencies
mainMenu = os.path.dirname(__file__).split('/')[-2]
nuke.menu("Nuke").addCommand(mainMenu + '/WrapItUp', 'import WrapItUp ; WrapItUp.WrapItUp( nodenamefolder=False, fonts=False, parentdircount=2, gizmos=False)', icon='pbicon.png')