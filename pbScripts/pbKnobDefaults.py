import nuke
import os
import math

#more recent items
m = nuke.menu("Nuke").findItem("File")
m.addCommand ("Open Recent Comp/@recent_file7", "nuke.scriptOpen(nuke.recentFile(7))", "")
m.addCommand ("Open Recent Comp/@recent_file8", "nuke.scriptOpen(nuke.recentFile(8))", "")
m.addCommand ("Open Recent Comp/@recent_file9", "nuke.scriptOpen(nuke.recentFile(9))", "")
m.addCommand ("Open Recent Comp/@recent_file10", "nuke.scriptOpen(nuke.recentFile(10))", "")
m.addCommand ("Open Recent Comp/@recent_file11", "nuke.scriptOpen(nuke.recentFile(11))", "")
m.addCommand ("Open Recent Comp/@recent_file12", "nuke.scriptOpen(nuke.recentFile(12))", "")
m.addCommand ("Open Recent Comp/@recent_file13", "nuke.scriptOpen(nuke.recentFile(13))", "")
m.addCommand ("Open Recent Comp/@recent_file14", "nuke.scriptOpen(nuke.recentFile(14))", "")
m.addCommand ("Open Recent Comp/@recent_file15", "nuke.scriptOpen(nuke.recentFile(15))", "")
m.addCommand ("Open Recent Comp/@recent_file16", "nuke.scriptOpen(nuke.recentFile(16))", "")
m.addCommand ("Open Recent Comp/@recent_file17", "nuke.scriptOpen(nuke.recentFile(17))", "")
m.addCommand ("Open Recent Comp/@recent_file18", "nuke.scriptOpen(nuke.recentFile(18))", "")
m.addCommand ("Open Recent Comp/@recent_file19", "nuke.scriptOpen(nuke.recentFile(19))", "")
m.addCommand ("Open Recent Comp/@recent_file20", "nuke.scriptOpen(nuke.recentFile(20))", "")
m.addCommand ("Open Recent Comp/@recent_file21", "nuke.scriptOpen(nuke.recentFile(21))", "")
m.addCommand ("Open Recent Comp/@recent_file22", "nuke.scriptOpen(nuke.recentFile(22))", "")




# Personal Default Node Settings
nuke.knobDefault('PostageStamp.label','[file tail [knob [topnode].file]]')
nuke.knobDefault('PostageStamp.hide_input','1')
nuke.knobDefault('DirBlurWrapper.BlurType','linear')


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
nuke.knobDefault('Roto.cliptype','no clip')
nuke.knobDefault('Radial.cliptype','no clip')
nuke.knobDefault('RotoPaint.cliptype','no clip')

nuke.knobDefault('FilterErode.filter','gaussian')

# channels to rgba
nuke.knobDefault('Defocus.channels','rgba')
nuke.knobDefault('Blur.channels','rgba')
nuke.knobDefault('Multiply.channels','rgba')
nuke.knobDefault('Add.channels','rgba')
nuke.knobDefault('Gamma.channels','rgba')
nuke.knobDefault('Dissolve.channels','rgba')
nuke.knobDefault('Keymix.channels','rgba')
nuke.knobDefault('Constant.channels','rgba')
nuke.knobDefault('Dilate.channels','rgba')
nuke.knobDefault('Erode.channels','rgba')
nuke.knobDefault('FilterErode.channels','rgba')
nuke.knobDefault('DirBlurWrapper.BlurLayer','rgba')
nuke.knobDefault("STMap.uv","rgb")

#nuke.knobDefault("Write.mov.colorspace", "")
#nuke.knobDefault("Write.mov.codec","apch")
#nuke.knobDefault("Write.mov.mov64_codec", "apch")

# copy to layerCopy
nuke.knobDefault('Copy.from0','none')
nuke.knobDefault('Copy.to0','none')
nuke.knobDefault('Copy.channels','alpha')

nuke.knobDefault("Write.label", "[ lindex [split [filename] /] end-2]")

#framehold to current frame as default
nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )", icon='FrameHold.png')


p = nuke.toNode('preferences')
p['maxPanels'].setValue('2')
p['reopenMovesPanel'].setValue(True)
p['ExpandSelection'].setValue(True)
p['ArrowColorUp'].setValue(0xff0000ff) # red color








#.singleValue()