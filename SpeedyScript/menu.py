mainMenu = menuMaker()

nuke.menu('Nuke').addCommand(mainMenu + 'Speedy Script/import script as Group', "import SpeedyScript ; SpeedyScript.importScriptFunction(nuke.getFilename('Please Select'))", icon='SpeedyScript.png')
nuke.menu('Nuke').addCommand(mainMenu + 'Speedy Script/Export Group as Grizmo', "import SpeedyScript ; SpeedyScript.exportScriptFunction()", icon='SpeedyScript.png')
nuke.menu('Nuke').addCommand(mainMenu + 'Speedy Script/Find Imported Group', "import SpeedyScript ; SpeedyScript.findGroupFunction()", icon='SpeedyScript.png')