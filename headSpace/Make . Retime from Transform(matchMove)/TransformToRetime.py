import nuke
import math

# ------------------------------------------------------------
# Helper math functions
# ------------------------------------------------------------

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def interp(a, b, p):
    """
    Closest point to p on segment a-b.
    Returns (x, y, weight) or None.
    """
    if a == b:
        return None

    ap = (p[0] - a[0], p[1] - a[1])
    ab = (b[0] - a[0], b[1] - a[1])

    ab_len2 = ab[0] ** 2 + ab[1] ** 2
    if ab_len2 == 0:
        return None

    w = max(0.0, min(1.0, (ap[0] * ab[0] + ap[1] * ab[1]) / ab_len2))
    return (a[0] + ab[0] * w, a[1] + ab[1] * w, w)

def as_vec2(value):
    """
    Normalize Nuke knob values to (x, y)
    Handles floats, lists, and tuples.
    """
    if isinstance(value, (list, tuple)):
        return (value[0], value[1])
    return (value, 0.0)

def apply_axis(v, axis):
    if axis == "X":
        return (v[0], 0.0)
    elif axis == "Y":
        return (0.0, v[1])
    return v  # Both

# ------------------------------------------------------------
# Main tool
# ------------------------------------------------------------

def retime_tracked_transform():

    # --------------------------------------------------------
    # Selection validation
    # --------------------------------------------------------

    nodes = nuke.selectedNodes()
    if len(nodes) != 2:
        nuke.message(
            "Select exactly TWO Transform nodes:\n\n"
            "1) Smooth animation (select first)\n"
            "2) Jerky animation (select second)"
        )
        return

    smooth, jerky = nodes[0], nodes[1]

    if smooth.Class() != "Transform" or jerky.Class() != "Transform":
        nuke.message("Both selected nodes must be Transform nodes.")
        return

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    root = nuke.Root()
    script_first = int(root["first_frame"].value())
    script_last = int(root["last_frame"].value())

    panel = nuke.Panel("Retime Jerky Transform")
    panel.addEnumerationPulldown("Curve", "translate rotation scale")
    panel.addEnumerationPulldown("Axis", "Both X Y")
    panel.addEnumerationPulldown("Output Node", "OFlow Kronos TimeWarp")
    panel.addBooleanCheckBox("Use Custom Frame Range", False)
    panel.addSingleLineInput("Start Frame", str(script_first))
    panel.addSingleLineInput("End Frame", str(script_last))

    if not panel.show():
        return

    curve = panel.value("Curve")
    axis = panel.value("Axis")
    output_type = panel.value("Output Node")
    use_custom = panel.value("Use Custom Frame Range")

    try:
        start = int(panel.value("Start Frame"))
        end = int(panel.value("End Frame"))
    except ValueError:
        nuke.message("Start Frame and End Frame must be integers.")
        return

    # --------------------------------------------------------
    # Frame range resolution
    # --------------------------------------------------------

    if use_custom:
        start = max(script_first, start)
        end = min(script_last, end)

        if start >= end:
            nuke.message("Invalid frame range.")
            return
    else:
        start = script_first
        end = script_last

    frames = list(range(start, end + 1))
    length = len(frames)

    jerky_vals = []
    smooth_vals = []

    # --------------------------------------------------------
    # Sample curves safely
    # --------------------------------------------------------

    for f in frames:

        if curve == "translate":
            j = apply_axis(as_vec2(jerky["translate"].valueAt(f)), axis)
            s = apply_axis(as_vec2(smooth["translate"].valueAt(f)), axis)

        elif curve == "scale":
            j = apply_axis(as_vec2(jerky["scale"].valueAt(f)), axis)
            s = apply_axis(as_vec2(smooth["scale"].valueAt(f)), axis)

        elif curve == "rotation":
            j = (jerky["rotate"].valueAt(f), 0.0)
            s = (smooth["rotate"].valueAt(f), 0.0)

        jerky_vals.append(j)
        smooth_vals.append(s)

    # --------------------------------------------------------
    # Create output retime node
    # --------------------------------------------------------

    if output_type == "OFlow":
        out = nuke.createNode("OFlow2", "timing2 Frame")
        timing_knob = out["timingFrame2"]

    elif output_type == "Kronos":
        out = nuke.createNode("Kronos", "timing2 Frame")
        timing_knob = out["timingFrame2"]

    else:  # TimeWarp
        out = nuke.createNode("TimeWarp")
        timing_knob = out["lookup"]

    timing_knob.setAnimated()
    out.setInput(0, jerky)

    # --------------------------------------------------------
    # Retiming logic
    # --------------------------------------------------------

    for i in range(length):
        target = smooth_vals[i]

        closest = min(
            range(length),
            key=lambda x: distance(jerky_vals[x], target)
        )

        before = None
        after = None

        if closest > 0:
            before = interp(jerky_vals[closest], jerky_vals[closest - 1], target)

        if closest < length - 1:
            after = interp(jerky_vals[closest], jerky_vals[closest + 1], target)

        offset = 0.0

        if before is not None and after is not None:
            offset = -before[2] if distance(before, target) < distance(after, target) else after[2]
        elif before is not None:
            offset = -before[2]
        elif after is not None:
            offset = after[2]

        timing_knob.setValueAt(start + closest + offset, frames[i])

    # --------------------------------------------------------
    # Done
    # --------------------------------------------------------

    nuke.message(
        "Retime complete ✔\n\n"
        "Curve: {}\n"
        "Axis: {}\n"
        "Frames: {}–{}\n"
        "Output: {}".format(
            curve.capitalize(),
            axis,
            start,
            end,
            output_type
        )
    )

# ------------------------------------------------------------
# Execute
# ------------------------------------------------------------

#retime_tracked_transform()
