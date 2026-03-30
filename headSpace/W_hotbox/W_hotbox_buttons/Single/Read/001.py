#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set Project
#
#----------------------------------------------------------------------------------------------------------

node = nuke.selectedNode()

first = node.knob('first').value()
last = node.knob('last').value()
Format = node.knob('format').value()
fps = node.metadata('input/frame_rate')
rng = last-first

if rng == 0: last = 99 

nuke.Root().knob('first_frame').setValue(first)
nuke.Root().knob('last_frame').setValue(last)
nuke.Root().knob('lock_range').setValue(True)
nuke.Root().knob('format').setValue(Format)
nuke.Root().knob('fps').setValue(fps)

if nuke.frame() not in range(first,last+1):
    nuke.frame(first)

print (fps)