mainMenu = menuMaker()
nuke.menu("Nuke").addCommand(mainMenu + 'Gizmo to group','import gizmoToGroup ; gizmoToGroup.convertGizmosToGroups()','Ctrl+shift+g', icon='pbicon.png')
