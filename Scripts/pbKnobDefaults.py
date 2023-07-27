import nuke
import os
import math

#more recent items
menubar = nuke.menu("Nuke");
m = menubar.findItem("File")
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
nuke.knobDefault('DirBlurWrapper.BlurLayer','rgba')

nuke.knobDefault('Merge2.bbox','B')
nuke.knobDefault('Keymix.bbox','B')

nuke.knobDefault('zoom_window_behaviour', '3')

nuke.knobDefault('Multiply.value','0')
nuke.knobDefault('Multiply.invert_mask','0')

nuke.knobDefault('EXPTool.mode','0')
nuke.knobDefault('Blur.size','2')

nuke.knobDefault("STMap.uv","rgb")

nuke.knobDefault('Read.auto_alpha','true')
nuke.knobDefault('Viewer.full_frame_processing','true')
nuke.knobDefault('Viewer.gl_lighting','true')

nuke.knobDefault('Roto.cliptype','no clip')
nuke.knobDefault('Radial.cliptype','no clip')
nuke.knobDefault('RotoPaint.cliptype','no clip')

nuke.knobDefault('FilterErode.filter','gaussian')

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

#nuke.knobDefault("Write.mov.colorspace", "")
#nuke.knobDefault("Write.mov.codec","apch")
#nuke.knobDefault("Write.mov.mov64_codec", "apch")

nuke.knobDefault("Write.label", "[ lindex [split [filename] /] end-2]")


p = nuke.toNode('preferences')
p['maxPanels'].setValue('2')
p['reopenMovesPanel'].setValue(True)
p['ExpandSelection'].setValue(True)
p['ArrowColorUp'].setValue(0xff0000ff) # red color






def pbAutoLabel():

    #Icons visiblillity (from nuke autolabal)
    ind = nuke.expression("(keys?1:0)+(has_expression?2:0)+(clones?8:0)+(viewsplit?32:0)")
    if int(nuke.numvalue("maskChannelInput", 0)) :
        ind += 4
    if int(nuke.numvalue("this.mix", 1)) < 1:
        ind += 16
    nuke.knob("this.indicators", str(ind))

    this = nuke.toNode("this")

    # do stuff that works even if autolabel is turned off:
    name = nuke.value("name")
    _class = this.Class()

    label = nuke.value("label")
    if not label:
        label = ""
    else:
        try:
            label = nuke.tcl("subst", label)
        except:
            pass



    #Custom values added here per node class-----------------------------

    n = nuke.thisNode()
    if n.Class() != 'Dot' or 'BackdropNode' or 'StickyNote':
        autoLabel = n.name()
    if n.Class() == "Blur":
        autoLabel += ' (' + str(math.ceil(n['size'].value())) + ')' 
        if not n['channels'].value() == 'rgba':
            autoLabel += '\n' + ' (' + n['channels'].value() + ')'

    elif n.Class() == "Defocus":
        autoLabel += ' (' + str(math.ceil(n['defocus'].value())) + ')' 
        if not n['channels'].value() == 'rgba':
            autoLabel += '\n' + ' (' + n['channels'].value() + ')'

    elif n.Class() == "Shuffle2":
        autoLabel += ' (' + str(n['in1'].value()) + '->' + str(n['out1'].value()) + ')'

    elif n.Class() == "FilterErode" or n.Class() == "Dilate" or n.Class() == "Erode":
        autoLabel += ' (' + str(math.ceil(n['size'].value())) + ')'

    elif n.Class() == "Multiply" or n.Class() == "Add" or n.Class() == "Gamma":
        autoLabel += ' (' + str(n['value'].value()) + ')'
        if not n['channels'].value() == 'rgba':
            autoLabel += '\n' + ' (' + n['channels'].value() + ')'

    elif n.Class() == "EXPTool":
        autoLabel += ' (' + str(n['red'].value()) + ')'
        if not n['red'].value() == n['green'].value() == n['blue'].value():
            autoLabel += '\n' + ' (' + str(n['red'].value()) + ',' + str(n['green'].value()) + ',' + str(n['blue'].value()) + ')'

    elif n.Class() == "Switch" or n.Class() == "Dissolve":
        autoLabel += ' (' + str(n['which'].value()) + ')'

    elif n.Class() == "TimeOffset":
        frame = nuke.frame()
        if n["reverse_input"].value():
            if n.input(0):
                first_frame = n.input(0).frameRange().first()
                last_frame = n.input(0).frameRange().last()
            else:
                first_frame = nuke.root().firstFrame()
                last_frame = nuke.root().lastFrame()
            reverse = -1 * frame + first_frame + last_frame
            offset_num = int(reverse + offset)
            input_frame = "input frame: %d\nREVERSED" % offset_num
        else:
            input_frame = "input frame: %d" % int(frame - offset)
        autolabel +=" (" + str(offset) + ")", input_frame



    #add mask and premult info irrispective of nodeClass (from nuke autolabal)

    layer = nuke.value("this.output", nuke.value("this.channels", "-"))
    mask = nuke.value("this.maskChannelInput", "none")
    unpremult = nuke.value("this.unpremult", "none")

    if mask != "none":
        if int(nuke.numvalue("invert_mask", 0)):
            layer += (" / ~" + mask)
        else:
            layer += (" / " + mask)

    if unpremult != "none" and unpremult != mask and _class.find("Deep", 0) == -1:
        layer += ( " / " + unpremult)

    # filePath = nuke.value("this.file", "none")

    # if filePath != "none":
    #     layer += ( " \n " + unpremult)



    #append user label if exists (from nuke autolabal)-----------------
    label = nuke.value("label")
    if not label:
        label = ""
    else:
        try:
          label = nuke.tcl("subst", label)
          autoLabel += '\n' + label
        except:
          pass

    

    return autoLabel

 
nuke.addAutolabel(pbAutoLabel)

#.singleValue()