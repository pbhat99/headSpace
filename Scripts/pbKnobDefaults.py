import nuke
import os

#more recent items
menubar = nuke.menu("Nuke");
m = menubar.addMenu("File")
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
nuke.knobDefault('Erode.channels','rgba')
nuke.knobDefault('PostageStamp.label','[file tail [knob [topnode].file]]')
nuke.knobDefault('PostageStamp.hide_input','1')
nuke.knobDefault('DirBlurWrapper.BlurType','linear')
nuke.knobDefault('DirBlurWrapper.BlurLayer','rgba')
nuke.knobDefault('Merge2.bbox','B')

nuke.knobDefault('Keymix.bbox','B')

nuke.knobDefault('zoom_window_behaviour', '3')

nuke.knobDefault('Multiply.value','0')
nuke.knobDefault('Multiply.invert_mask','0')


nuke.knobDefault('Blur.channels','rgba')
nuke.knobDefault('Blur.size','2')

nuke.knobDefault("STMap.uv","rgb")

nuke.knobDefault('Read.auto_alpha','true')
nuke.knobDefault('Viewer.full_frame_processing','true')
nuke.knobDefault('Viewer.gl_lighting','true')
#nuke.knobDefault('BackdropNode.note_font_size','99')

nuke.knobDefault('Roto.cliptype','no clip')
nuke.knobDefault('Radial.cliptype','no clip')
nuke.knobDefault('RotoPaint.cliptype','no clip')

nuke.knobDefault('FilterErode.filter','gaussian')

nuke.knobDefault('Defocus.channels','rgba')
nuke.knobDefault('Keymix.channels','rgba')
nuke.knobDefault('Constant.channels','rgba')
nuke.knobDefault('Dilate.channels','rgba')
nuke.knobDefault('Erode.channels','rgba')
nuke.knobDefault('FilterErode.channels','rgba')

#nuke.knobDefault("Write.mov.colorspace", "MillView")
#nuke.knobDefault("Write.mov.codec","apch")
#nuke.knobDefault("Write.mov.mov64_codec", "apch")

nuke.knobDefault("Write.label", "[ lindex [split [filename] /] end-2]")

#nuke.knobDefault("Shuffle2.autolabel","nuke.thisNode().name() + ' (' + str(nuke.thisNode()['in1'].value()) + '->' + str(nuke.thisNode()['out1'].value()) + ')'")
#nuke.knobDefault("Shuffle.autolabel","nuke.thisNode().name() + ' (' + str(nuke.thisNode()['in1'].value()) + '->' + str(nuke.thisNode()['out1'].value()) + ')'")






def nodeAutoLabel():
    n = nuke.thisNode()
    if n.Class() == "Blur":
        autoLabel = n.name() + ' (' + str(n['size'].value()) + ')' 
        if not n['channels'].value() == 'rgba':
            autoLabel = autoLabel + '\n' + n['channels'].value()
        if n['label'].value():
            autoLabel = autoLabel + '\n' + n['label'].value()
        return autoLabel

    if n.Class() == "Defocus":
        autoLabel = n.name() + ' (' + str(n['defocus'].value()) + ')' 
        if not n['channels'].value() == 'rgba':
            autoLabel = autoLabel + '\n' + n['channels'].value()
        if n['label'].value():
            autoLabel = autoLabel + '\n' + n['label'].value()
        return autoLabel

    if n.Class() == "Shuffle2":
        autoLabel = n.name() + ' (' + str(n['in1'].value()) + '->' + str(n['out1'].value()) + ')'
        if n['label'].value():
            autoLabel = autoLabel + '\n' + n['label'].value()
        return autoLabel

    if n.Class() == "FilterErode" or n.Class() == "Dilate" or n.Class() == "Erode":
        autoLabel = n.name() + ' (' + str(n['size'].value()) + ')'
        if n['label'].value():
            autoLabel = autoLabel + '\n' + n['label'].value()
        return autoLabel
 
nuke.addAutolabel(nodeAutoLabel)


