mainMenu = menuMaker()


#nuke.menu("Nuke").addCommand(mainMenu + 'GUI Disable', 'nuke.load("guiTool") , disableGUI()','^+D', icon='pbicon.png')
nuke.menu("Nuke").addCommand(mainMenu + 'GUI tool', 'nuke.load("guiTool") , guiTool()','+D', icon='pbicon.png')
