#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Remove Static Animation
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    for knob_name in node.knobs():
        knob = node[knob_name]
        array_size = knob.arraySize() if hasattr(knob, 'arraySize') else 1

        for i in range(array_size):
            if knob.hasExpression(i) or not knob.isAnimated(i):
                continue

            curve = knob.animation(i)
            keyframes = curve.keys()
            key_values = list(set([k.y for k in keyframes]))

            if len(key_values) <= 1:
                knob.clearAnimated(i)
                print(f"Removed static animation from: {node.name()}.{knob_name}[{i}]")
