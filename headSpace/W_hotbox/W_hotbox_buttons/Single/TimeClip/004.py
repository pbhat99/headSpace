#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: TO in/out
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    activeViewer = nuke.activeViewer().node()
    print (activeViewer)
    activeViewer.knob('frame_range').setValue(str(i.knob('first').value())+ '-'+ str(i.knob('last').value()))
    activeViewer.knob('frame_range_lock').setValue(True)
    activeViewer.redraw()