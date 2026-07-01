import collections
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

    if n.Class() in ("Transform", "CornerPin2D", "Card3D", "MotionBlur2D", "Tracker4"):
        addIndicators()
        if n.Class() == "Tracker4":
            aLabel.append(f"{n.name()} [{n['reference_frame'].value()}]")
            transform = n["transform"].value()
            if transform != "none":
                aLabel.append(transform)
        else:
            aLabel.append(n.name())
            inv = n.knob("invert_matrix") or n.knob("invert")
            if inv and inv.value():
                aLabel.append("[inverted]")
        motionblur , shutter = n.knob("motionblur") , n.knob("shutter")
        if n.Class() == "MotionBlur2D" or (motionblur and motionblur.value()):
            aLabel.append(f"[mb : {n['shutteroffset'].value()} ~ {trimTo2Dec(shutter.value())}]")

        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()


    if n.Class() == "Mirror2":
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
        for knob in ("channels", "channels2", "channels3", "channels4"):
            value = n[knob].value()
            if value != "none":
                aLabel.append(f"({value})")
        aLabel.append(n["label"].evaluate() or "")
        return "\n".join(aLabel).strip()

    # if n.Class() in ("Shuffle2"):
    #     addIndicators()
    #     out_layer = n["out1"].value()
    #     mappings = n["mappings"].value()
    #     src_channels, dst_channels, src_layers = [],[],[]

    #     for m in mappings:
    #         try:
    #             src, dst = m[1], m[2] 
    #             src_layer, src_chan = src.split(".")
    #             dst_layer, dst_chan = dst.split(".")
    #             # collect unique source layers
    #             if src_layer not in src_layers:
    #                 src_layers.append(src_layer)
    #             # skip black inputs
    #             if src_layer == "black":
    #                 continue
    #             src_channels.append(src_chan)
    #             dst_channels.append(dst_chan)
    #         except:
    #             pass

    #     src_layer_text = "-".join(src_layers) if src_layers else "?"

    #     aLabel.append("%s [%s -> %s]\n%s -> %s" % (
    #         n.name(),
    #         src_layer_text,
    #         n["out1"].value(),
    #         "-".join(src_channels),
    #         "-".join(dst_channels)
    #     ))
    #     aLabel.append(n["label"].evaluate() or "")
    #     return "\n".join(aLabel).strip()



nuke.addAutolabel(pbAutoLabel)