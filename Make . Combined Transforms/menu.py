
mainMenu = menuMaker()
nuke.menu("Nuke").addCommand(mainMenu + 'Combine Transforms', 'import mergeTransforms ; mergeTransforms.start()', '')
