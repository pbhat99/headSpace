import nuke
import math

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
    autoLabel = nuke.thisNode().name()

    if n.Class() != 'Dot' or 'BackdropNode' or 'StickyNote':
        autoLabel = label

    if label != '':
        label = '\n' + label

    if n.Class() == "Blur":
        autoLabel += ' (' + str(math.ceil(n['size'].value())) + ')' 
        if not n['channels'].value() == 'rgba':
            autoLabel += '\n' + ' (' + n['channels'].value() + ')' + label

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
            autoLabel += '\n' + ' (' + n['channels'].value() + ')' + label

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


    return autoLabel

 
nuke.addAutolabel(pbAutoLabel)
