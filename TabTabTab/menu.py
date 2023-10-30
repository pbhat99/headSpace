#TabTabTab (tab with menu items search)

mainMenu = os.path.dirname(__file__).split('/')[-2]
nuke.menu("Nuke").addCommand(mainMenu + '/TabTabTab', 'import tabtabtab ; tabtabtab.main()', 'Ctrl+Tab', shortcutContext=2, icon='pbicon.png')