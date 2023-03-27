#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Frame handle
#
#----------------------------------------------------------------------------------------------------------

def ToggleFrameRange():
    offset = 10
    firstFrame = int(nuke.Root().knob('first_frame').value())
    lastFrame = int(nuke.Root().knob('last_frame').value())
    activeViewer = nuke.activeViewer().node()
    if int(activeViewer .knob('frame_range').value().rpartition("-")[0]) != firstFrame+offset:
        activeViewer .knob('frame_range').setValue('%i-%i'%(firstFrame + offset,lastFrame - offset))
    else:
        activeViewer .knob('frame_range').setValue(str(firstFrame)+"-"+str(lastFrame))
    activeViewer .knob('frame_range_lock').setValue(True)
    
ToggleFrameRange()