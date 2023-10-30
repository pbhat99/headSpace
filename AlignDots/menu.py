# dot create and align tool
mainMenu = os.path.dirname(__file__).split('/')[-2] + '/NodeGraph/Align Dots'

nuke.menu('Nuke').addCommand(mainMenu, "import AlignDots ; AlignDots.AlignDots()", 'Shift+.', shortcutContext=2, icon='pbicon.png')