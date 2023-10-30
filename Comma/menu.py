# comma tool
mainMenu = os.path.dirname(__file__).split('/')[-2]

nuke.menu("Nuke").addCommand(mainMenu + '/Utilities/Comma','import comma ; comma.makeComma()',',',icon='Comma.png')