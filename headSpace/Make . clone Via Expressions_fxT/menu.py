# remove original clone entries from the nuke menu
#edit_menu = menubar.findItem('&Edit')
#edit_menu.removeItem("Clone")
#edit_menu.removeItem("Declone")
#edit_menu.removeItem("Copy As Clones")
#edit_menu.removeItem("Force Clone")


mainMenu = menuMaker()

nuke.menu('Nuke').addCommand(mainMenu + '-', '', '')
nuke.menu("Nuke").addCommand(mainMenu + 'Clone via Expression', 'import fxT_cloneViaExpressions ; fxT_cloneViaExpressions.clone_via_expression()', '+k', icon='pbicon.png')
nuke.menu("Nuke").addCommand(mainMenu + 'Declone Expression', 'import fxT_cloneViaExpressions ; fxT_cloneViaExpressions.clear_expression()', '^+k', icon='pbicon.png')
