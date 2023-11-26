#mainMenu = os.path.dirname(__file__).split('/')[-2]
mainMenu = menuMaker()
nuke.menu("Nuke").addCommand(mainMenu + 'Tracket to Transform' , 'import trackerToTransform ; trackerToTransform.trackerToTransform()', icon='pbicon.png')
