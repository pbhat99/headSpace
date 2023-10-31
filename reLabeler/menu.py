# comma tool

import labeler
def relabel():
    """ Change the node(s) label"""
    global relabel_popup
    relabel_popup = labeler.Labeller()
    relabel_popup.run()

mainMenu = os.path.dirname(__file__).split('/')[-2]

nuke.menu("Nuke").addCommand(mainMenu + '/Utilities/Re-Label Nodes', relabel, 'n', shortcutContext=2, icon = 'label_node.png')