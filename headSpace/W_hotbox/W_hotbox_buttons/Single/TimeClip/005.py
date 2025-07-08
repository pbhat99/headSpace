#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: FROM in/out
#
#----------------------------------------------------------------------------------------------------------

activeViewer = nuke.activeViewer().node()
frange = activeViewer.knob('frame_range').value()

for i in nuke.selectedNodes():
    i.knob('first').setValue(int(frange.split('-')[0]))
    i.knob('last').setValue(int(frange.split('-')[1]))