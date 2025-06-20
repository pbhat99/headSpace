mainMenu = menuMaker()
nuke.menu('Nuke').addCommand(mainMenu + 'Speedy Script/Speedy import script', "import SpeedyScriptLight ; SpeedyScriptLight.importScriptFunction(nuke.getFilename('Please Select'))", icon='SpeedyScript.png')
nuke.menu('Nuke').addCommand(mainMenu + 'Speedy Script/Speedy Export Group', "import SpeedyScriptLight ; SpeedyScriptLight.exportScriptFunction()", icon='SpeedyScript.png')
nuke.menu('Nuke').addCommand(mainMenu + 'Speedy Script/Speedy Find Group', "import SpeedyScriptLight ; SpeedyScriptLight.findGroupFunction()", icon='SpeedyScript.png')