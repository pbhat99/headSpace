import W_moveMenu

mainMenu = os.path.dirname(__file__).split('/')[-2]

W_moveMenu.moveMenus(['Edit/W_hotbox', 'Edit/Knob Scripter', 'Edit/Stamps' ], mainMenu, sourceRoot = 'Nuke', destinationRoot = 'Nuke')