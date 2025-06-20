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
        aLabel.append(n.name() + ' [' + str(n['defocus'].value())+ ']')
        aLabel if n["channels"].value() == "rgba" else aLabel.append('(' + str(n["channels"].value() + ')'))
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() == "Blur":
        addIndicators()
        aLabel.append(n.name() + ' [' + str(n['size'].value())+ ']')
        aLabel if n["channels"].value() == "rgba" else aLabel.append('(' + str(n["channels"].value() + ')'))
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() == "Transform":
        addIndicators()
        aLabel.append(n.name())
        aLabel if n["invert_matrix"].value() == False else aLabel.append('[inverted]')
        aLabel if n["motionblur"].value() == False else aLabel.append('[mb : ' + str(n['motionblur'].value()).rstrip('.0') + ' ~ ' +  str(n['shutter'].value()).rstrip('.0') + ']')
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

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

    if n.Class() == "Remove":
        addIndicators()
        aLabel.append(n.name() + ' [' + str(n['operation'].value())+ ']')
        aLabel if n["channels"].value() == "none" else aLabel.append('(' + str(n["channels"].value() + ')'))
        aLabel if n["channels2"].value() == "none" else aLabel.append('(' + str(n["channels2"].value() + ')'))
        aLabel if n["channels3"].value() == "none" else aLabel.append('(' + str(n["channels3"].value() + ')'))
        aLabel if n["channels4"].value() == "none" else aLabel.append('(' + str(n["channels4"].value() + ')'))
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()
       
nuke.addAutolabel(pbAutoLabel)