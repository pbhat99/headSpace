# Maya like hotbox control for Nuke
import W_hotbox
import W_hotboxManager

p = nuke.toNode('preferences')
p.knob('hotboxLocation').setValue(__file__.replace('menu.py', 'W_hotbox_buttons'))
p.knob('hotboxIconLocation').setValue(__file__.replace('menu.py', 'W_hotbox_icons'))
savePreferencesToFile()