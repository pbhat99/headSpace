mainMenu = menuMaker()

nuke.menu('Nuke').addCommand(mainMenu + 'Delete Viewers inside Groups', "import deleteGroupViewers ; deleteGroupViewers.delViewers()" )