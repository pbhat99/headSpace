# Maya like hotbox control for Nuke
import W_hotbox
import W_hotboxManager
nuke.toNode('preferences')['hotboxLocation'].setValue(__file__.replace('menu.py', 'W_hotbox_buttons'))
nuke.toNode('preferences')['hotboxIconLocation'].setValue(__file__.replace('menu.py', 'W_hotbox_icons'))