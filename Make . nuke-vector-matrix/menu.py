
mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + "Convert Transforms", 'import matrix_utils ; matrix_utils.run_convert_matrix()')
nuke.menu("Nuke").addCommand(mainMenu + "Merge Transforms", 'import matrix_utils ; matrix_utils.run_merge_transforms()')
nuke.menu("Nuke").addCommand(mainMenu + "Convert Tracker to SplineWarp", 'import matrix_utils ; matrix_utils.run_convert_tracker_to_splinewarp()')

# Menus in the animation menu must call a string for some reason
nuke.menu('Animation').addCommand('Edit/Filter Rotations',
                                  "from transform_utils import rotation_filters;"
                                  "rotation_filters.setup_filter_rotations()")


