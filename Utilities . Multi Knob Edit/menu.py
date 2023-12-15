mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'Toggle Multi Knob Edit Mode', 'import MultiKnobEdit ; MultiKnobEdit.multiEditExec()' , '#m' , icon = 'Matrix.png')
