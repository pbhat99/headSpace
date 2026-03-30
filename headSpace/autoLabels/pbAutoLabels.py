import nuke
import os
import math

def trimTo2Dec(value):
    def _one(x):
        # Round up to 2 decimal places
        x_rounded = math.ceil(x * 100.0) / 100.0
        s = f"{x_rounded:.2f}"
        return s.rstrip('0').rstrip('.') if '.' in s else s
    if isinstance(value, (list, tuple)):
        return ", ".join(_one(x) for x in value)
    return _one(value)

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
        aLabel.append(f"{n.name()} [{trimTo2Dec(n['defocus'].value())}]")
        if n["channels"].value() != "rgba":
            aLabel.append(f'({n["channels"].value()})')
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() in ("Blur", "Erode", "Dilate", "FilterErode", "EdgeBlur", "Median", "ZDefocus2", "Sharpen", "Soften"):
        addIndicators()
        aLabel.append(f"{n.name()} [{trimTo2Dec(n['size'].value())}]")
        if n["channels"].value() != "rgba":
            aLabel.append(f'({n["channels"].value()})')
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() in ("Transform", "CornerPin2D"):
        addIndicators()
        aLabel.append(n.name())
        # Check for inverted state (different knob names per node)
        inv = n.knob("invert_matrix") or n.knob("invert")
        if inv and inv.value():
            aLabel.append('[inverted]')
        if n["motionblur"].value():
            aLabel.append(f"[mb : {str(n['motionblur'].value()).rstrip('.0')} ~ {str(n['shutter'].value()).rstrip('.0')}]")
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() in ("Tracker4"):
        addIndicators()
        aLabel.append(f"{n.name()} [{trimTo2Dec(n['reference_frame'].value())}]")
        if n["transform"].value() != 'none':
            aLabel.append(n["transform"].value())
        if n["motionblur"].value():
            aLabel.append(f"[mb : {str(n['motionblur'].value()).rstrip('.0')} ~ {str(n['shutter'].value()).rstrip('.0')}]")
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()


    if n.Class() in ("Mirror", "Mirror2"):
        addIndicators()
        aLabel.append(n.name())
        m_label = []
        if n["flip"].value():
            m_label.append("vertical")
        if n["flop"].value():
            m_label.append("horizontal")
        if m_label:
            aLabel.append(f"[{' & '.join(m_label)}]")
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() in ("Read", "DeepRead", "TimeClip"):
        addIndicators()
        aLabel.append(n.name())
        
        file_knob = n.knob("file")
        range_str = f"[{int(n['first'].value())}-{int(n['last'].value())}]"
        
        if file_knob and file_knob.value():
            filename = os.path.basename(file_knob.value())
            aLabel.append(filename)
            
        if n.knob("raw") and n["raw"].value():
            aLabel.append("[RAW]")
        elif n.knob("colorspace"):
            aLabel.append(f"[{n['colorspace'].value()}]")
        
        aLabel.append(range_str)
            
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() == "ScanlineRender":
        addIndicators()
        aLabel.append(f"{n.name()} [{int(n['samples'].value())}]")
        if n["projection_mode"].value() != "render camera":
            aLabel.append(f'[{n["projection_mode"].value()}]')
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    if n.Class() in ("Remove"):
        addIndicators()
        aLabel.append(f"{n.name()} [{n['operation'].value()}]")
        if n["channels"].value() != "none":
            aLabel.append(f'({n["channels"].value()})')
        if n["channels2"].value() != "none":
            aLabel.append(f'({n["channels2"].value()})')
        if n["channels3"].value() != "none":
            aLabel.append(f'({n["channels3"].value()})')
        if n["channels4"].value() != "none":
            aLabel.append(f'({n["channels4"].value()})')
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()
       
nuke.addAutolabel(pbAutoLabel)