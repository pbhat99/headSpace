#mainMenu = os.path.dirname(__file__).split('/')[-2]
mainMenu = menuMaker()
nuke.menu("Nuke").addCommand(mainMenu + 'Retime From Transform' , 'import TransformToRetime ; TransformToRetime.retime_tracked_transform()', icon='pbicon.png')
