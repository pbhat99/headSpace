# dot create and align tool
mainMenu = os.path.dirname(__file__).split('/')[-2]

nuke.menu('Nuke').addCommand(mainMenu + '/NodeGraph/Align Dots', "import AlignDots ; AlignDots.AlignDots()", 'Shift+.', shortcutContext=2, icon='pbicon.png')