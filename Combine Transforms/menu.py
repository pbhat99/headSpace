mainMenu = os.path.dirname(__file__).split('/')[-2]

nuke.menu("Nuke").addCommand(mainMenu + '/Generate/Combine Transforms', 'import mergeTransforms ; mergeTransforms.start()', '')