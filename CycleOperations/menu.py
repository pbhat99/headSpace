#Cycle Operations
mainMenu = os.path.dirname(__file__).split('/')[-2]

nuke.menu('Nuke').addCommand(mainMenu + '/Cycle Operation/Forwards', "import CycleOperations ; CycleOperations.CycleOperations()", "]", shortcutContext=2, icon='pbicon.png')
nuke.menu('Nuke').addCommand(mainMenu + '/Cycle Operation/Backwards', "import CycleOperations ; CycleOperations.CycleOperations(False)", "[", shortcutContext=2, icon='pbicon.png')