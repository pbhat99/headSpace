#Cycle Operations
mainMenu = menuMaker()

nuke.menu('Nuke').addCommand(mainMenu + 'Auto Crop', "import autoCrop ; autoCrop.autoCrop()", icon='Crop.png')
