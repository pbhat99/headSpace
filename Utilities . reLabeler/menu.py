# comma tool

import labeler
def relabel():
    """ Change the node(s) label"""
    global relabel_popup
    relabel_popup = labeler.Labeller()
    relabel_popup.run()

mainMenu = menuMaker()

nuke.menu("Nuke").addCommand(mainMenu + 'Re-Label Nodes', relabel, 'n', shortcutContext=2, icon = 'label_node.png')
