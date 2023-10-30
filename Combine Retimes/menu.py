mainMenu = os.path.dirname(__file__).split('/')[-2]

nuke.menu("Nuke").addCommand(mainMenu + '/Generate/Combine Retimes', 'import combine_retimes ; combine_retimes.combineRetimes()', '')