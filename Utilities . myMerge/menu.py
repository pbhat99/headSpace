mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'myMerge', 'import myMerge ; myMerge.mergeThis()', 'm', shortcutContext=2, icon = 'Merge.png')