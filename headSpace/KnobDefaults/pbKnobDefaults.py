import nuke
import os
import math

# more recent items
# https://community.foundry.com/discuss/topic/137014/open-recent-comps-customize-it
for i in range(7,25+1):
    nuke.menu("Nuke").findItem("File").addCommand('Open Recent Comp/@recent_file{0}'.format(i), 'nuke.scriptOpen(nuke.recentFile({0}))'.format(i))



#-----------Personal Default Node Settings------------


nuke.knobDefault('PostageStamp.label','[file tail [knob [topnode].file]]')
nuke.knobDefault('PostageStamp.hide_input','1')
nuke.knobDefault('DirBlurWrapper.BlurType','linear')

# BBox
# No Clip to format
bBox = ["Merge2", "Keymix", "Copy", "ChannelMerge"]
for node in bBox:
    nuke.knobDefault(f"{node}.bbox", "B")

nuke.knobDefault('Merge2.bbox','B')
nuke.knobDefault('Keymix.bbox','B')

nuke.knobDefault('zoom_window_behaviour', '3')

nuke.knobDefault('Multiply.value','0')
nuke.knobDefault('Multiply.invert_mask','0')

nuke.knobDefault('EXPTool.mode','0')
nuke.knobDefault('Blur.size','2')

# font sizes
nuke.knobDefault("BackdropNode.note_font_size","55")
nuke.knobDefault("Dot.note_font_size","55")
nuke.knobDefault("StickyNote.note_font_size","55")

nuke.knobDefault('Read.auto_alpha','true')
nuke.knobDefault('Viewer.full_frame_processing','true')
nuke.knobDefault('Viewer.gl_lighting','true')

# No Clip to format
nodeClip = ["Roto", "RotoPaint", "Radial", "Ramp", "Rectangle", "Grid", "Text", "Text2"]
for node in nodeClip:
    nuke.knobDefault(f"{node}.cliptype", "no clip")

# Filter
nuke.knobDefault('FilterErode.filter','gaussian')
nuke.knobDefault('Retime.filter','none')
nuke.knobDefault("VectorBlur2.blur_uv","linear")
nuke.knobDefault("VectorBlur2.blur_type","uniform")

# All channels to rgba
nodeChannels_rgba = [
    'Defocus', 'Blur', 'EdgeBlur', 'Multiply', 'Add', 'Clamp', 'Gamma', 'Invert', 'Dissolve', 'Keymix', 'Constant', 'Dilate', 'Erode',
    'FilterErode', 'DirBlurWrapper', 'STMap', 'IDistort', 'VectorBlur2', 'Median', 'ZDefocus2', 'Sharpen', 'Soften'
]
for node in nodeChannels_rgba:
    nuke.knobDefault(f"{node}.channels", "rgba")

#nuke.knobDefault("Write.mov.colorspace", "")
#nuke.knobDefault("Write.mov.codec","apch")
#nuke.knobDefault("Write.mov.mov64_codec", "apch")
#nuke.knobDefault("Write.label", "[ lindex [split [filename] /] end-2]")

# copy to layerCopy
nuke.knobDefault('Copy.from0','none')
nuke.knobDefault('Copy.to0','none')
nuke.knobDefault('Copy.channels','alpha')

# B to alpha 
nuke.knobDefault('Shuffle.onCreate',"nk = nuke.thisNode()['in2'].setValue('alpha')")
nuke.knobDefault('Shuffle2.onCreate',"nk = nuke.thisNode()['in2'].setValue('alpha')")

#remove/keep
nuke.knobDefault('Remove.channels','rgba')
#nuke.knobDefault('Remove.label', '[if {[value channels] == "rgb"} {return "(rgb)"} [if {[value channels] == "rgba"} {return "(rgba)"}]] [if {[value channels2] !="none"} {return ([value channels2])} {}] [if {[value channels3] !="none"} {return ([value channels3])} {}] [if {[value channels4] !="none"} {return ([value channels4])} {}]') 
nuke.menu('Nodes').addCommand( "Channel/Keep(Remove)", "nuke.createNode('Remove')['operation'].setValue('keep')", icon='Remove.png')

#framehold to current frame as default
nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )", icon='FrameHold.png')




p = nuke.toNode('preferences')
p['maxPanels'].setValue('2')
p['reopenMovesPanel'].setValue(True)
p['ExpandSelection'].setValue(True)
p['ArrowColorUp'].setValue(0xff0000ff) # red color








#.singleValue()