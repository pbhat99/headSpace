# dot create and align tool
mainMenu = menuMaker()

nuke.menu('Nuke').addCommand(mainMenu + 'Align Dots', "import AlignDots ; AlignDots.AlignDots()", 'Shift+.', shortcutContext=2, icon='pbicon.png')
