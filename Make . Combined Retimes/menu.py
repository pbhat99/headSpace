mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'Combine Retimes', 'import combine_retimes ; combine_retimes.combineRetimes()', '')
