#Cycle Operations
mainMenu = menuMaker()

nuke.menu('Nuke').addCommand(mainMenu + 'Cycle Forwards', "import CycleOperations ; CycleOperations.CycleOperations()", "]", shortcutContext=2, icon='pbicon.png')
nuke.menu('Nuke').addCommand(mainMenu + 'Cycle Backwards', "import CycleOperations ; CycleOperations.CycleOperations(False)", "[", shortcutContext=2, icon='pbicon.png')
