import nuke
import os

def trimTo2Dec(value):
    if isinstance(value, (list, tuple)):
        return ", ".join(str("{0:.2f}".format(x)).rstrip('.0') for x in value)
    else:
        return str(round(value, 2)).rstrip('.0')

def pbAutoLabel():
    def addIndicators():
        ind = nuke.expression("(keys?1:0)+(has_expression?2:0)+(clones?8:0)+(viewsplit?32:0)")
        if int(nuke.numvalue("maskChannelInput", 0)) :
          ind += 4
        if int(nuke.numvalue("this.mix", 1)) < 1:
          ind += 16
        nuke.knob("this.indicators", str(ind))
    
    aLabel = []

    n = nuke.thisNode()

    if n.Class() == "Defocus":
        addIndicators()
        aLabel.append(n.name() + ' [' + str(round(n['defocus'].value(), 2)).strip('.0')+ ']')
        aLabel if n["channels"].value() == "rgba" else aLabel.append('(' + str(n["channels"].value() + ')'))
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() in ("Blur", "Erode", "Dilate", "FilterErode", "EdgeBlur", "Median", "ZDefocus2", "Sharpen", "Soften"):
        addIndicators()
        aLabel.append(n.name() + ' [' + trimTo2Dec(n['size'].value()) + ']')
        aLabel if n["channels"].value() == "rgba" else aLabel.append('(' + str(n["channels"].value() + ')'))
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() in ("Transform"):
        addIndicators()
        aLabel.append(n.name())
        aLabel if n["invert_matrix"].value() == False else aLabel.append('[inverted]')
        aLabel if n["motionblur"].value() == False else aLabel.append('[mb : ' + str(n['motionblur'].value()).rstrip('.0') + ' ~ ' +  str(n['shutter'].value()).rstrip('.0') + ']')
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() in ("CornerPin2D"):
        addIndicators()
        aLabel.append(n.name())
        aLabel if n["invert"].value() == False else aLabel.append('[inverted]')
        aLabel if n["motionblur"].value() == False else aLabel.append('[mb : ' + str(n['motionblur'].value()).rstrip('.0') + ' ~ ' +  str(n['shutter'].value()).rstrip('.0') + ']')
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() in ("Tracker4"):
        addIndicators()
        aLabel.append(n.name() + ' [' + trimTo2Dec(n['reference_frame'].value()) + ']' )
        aLabel if n["transform"].value() == 'none' else aLabel.append(n["transform"].value())
        aLabel if n["motionblur"].value() == False else aLabel.append('[mb : ' + str(n['motionblur'].value()).rstrip('.0') + ' ~ ' +  str(n['shutter'].value()).rstrip('.0') + ']')
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()


    # if n.Class() == "Mirror2":
    #     addIndicators()
    #     if n["flip"].value() == True:
    #         icnFlip = '[&#8644;]'
    #     elif n["flop"].value() == True:
    #         icnFlop = '[&#8645;]'
    #     else:
    #         icnFlip = ''
    #         icnFlop = ''
    #     aLabel.append(n.name())
    #     aLabel.append(icnFlip + icnFlop)
    #     aLabel.append(n["label"].evaluate() or "")
    #     return "\n".join(aLabel).strip()

    if n.Class() == "TimeClip":
        addIndicators()
        aLabel.append(n.name())
        aLabel.append('[' + str(n['first'].value()) + '-' + str(n['last'].value())+ ']')
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() == "ScanlineRender":
        addIndicators()
        aLabel.append(n.name() + ' [' + str(int(n['samples'].value()))+ ']')
        aLabel if n["projection_mode"].value() == "render camera" else aLabel.append('[' + str(n["projection_mode"].value()) + ']')
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() in ("Remove"):
        addIndicators()
        aLabel.append(n.name() + ' [' + str(n['operation'].value())+ ']')
        aLabel if n["channels"].value() == "none" else aLabel.append('(' + str(n["channels"].value() + ')'))
        aLabel if n["channels2"].value() == "none" else aLabel.append('(' + str(n["channels2"].value() + ')'))
        aLabel if n["channels3"].value() == "none" else aLabel.append('(' + str(n["channels3"].value() + ')'))
        aLabel if n["channels4"].value() == "none" else aLabel.append('(' + str(n["channels4"].value() + ')'))
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()
       
nuke.addAutolabel(pbAutoLabel)