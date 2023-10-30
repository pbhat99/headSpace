#W_smartAlign
mainMenu = os.path.dirname(__file__).split('/')[-2]
nuke.menu('Nuke').addCommand(mainMenu + '/NodeGraph/W_align Left', 'import W_smartAlign ; W_smartAlign.alignNodes("left")',"Alt+Shift+left", shortcutContext=2, icon='pbicon.png')
nuke.menu('Nuke').addCommand(mainMenu + '/NodeGraph/W_align Right', 'import W_smartAlign ; W_smartAlign.alignNodes("right")',"Alt+Shift+right", shortcutContext=2, icon='pbicon.png')
nuke.menu('Nuke').addCommand(mainMenu + '/NodeGraph/W_align Up',	'import W_smartAlign ; W_smartAlign.alignNodes("up")', "Alt+Shift+up", shortcutContext=2, icon='pbicon.png')
nuke.menu('Nuke').addCommand(mainMenu + '/NodeGraph/W_align Down', 'import W_smartAlign ; W_smartAlign.alignNodes("down")', "Alt+Shift+down", shortcutContext=2, icon='pbicon.png')
nuke.menu("Nuke").menu(mainMenu + '/NodeGraph').addSeparator()