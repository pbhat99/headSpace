#sbnAlignReadNodes
mainMenu = menuMaker()

nuke.menu('Nuke').addCommand(mainMenu + '-', '', '')
nuke.menu('Nuke').addCommand(mainMenu + 'Align Read Nodes  ' , 'import AlignReads ; AlignReads.sbnAlignNodes("default")', 'L', shortcutContext=2)
nuke.menu('Nuke').addCommand(mainMenu + 'Align Read Nodes (vertical)'   , 'import AlignReads ; AlignReads.sbnAlignNodes("vertical")', 'shift+L', shortcutContext=2)
nuke.menu('Nuke').addCommand(mainMenu + 'Align Read Nodes (horizontal)' , 'import AlignReads ; AlignReads.sbnAlignNodes("horizontal")', '', shortcutContext=2)
nuke.menu('Nuke').addCommand(mainMenu + 'Align Read Nodes (wave)'       , 'import AlignReads ; AlignReads.sbnAlignNodes("wave")', '', shortcutContext=2)
nuke.menu('Nuke').addCommand(mainMenu + 'Align Read Nodes (zigzag)'     , 'import AlignReads ; AlignReads.sbnAlignNodes("zigzag")', '', shortcutContext=2)
nuke.menu('Nuke').addCommand(mainMenu + '-', '', '')
