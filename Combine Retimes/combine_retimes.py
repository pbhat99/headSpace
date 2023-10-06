"""

combine_retimes_v1.0.py
Version: 1.0.0
Author: Guillermo Algora
Last Updated: Jul 31th, 2023

Combine Retimes is a python script that can combines a stack of multiple retiming nodes
(Retime, TimeWarp, Kronos, OFlow, TimeOffset and FrameHold) into a merged output (both a lookup table and a speed value).
In addition, it supports Switch and Dissolve nodes in the stack, although because of its nature take the later with a pinch of salt.

This script does not require installation and can be executed directly from the Nuke's Script Editor.
However, to install:

  1) Place 'combine_retimes.py' in a directory that is part of the Nuke plugin path (to find out these directories
                                                                                   execute: "nuke.pluginPath()").

  2) In a 'menu.py' file: choose a menu and add the command "import combine_retimes".

     e.g.
            "combine_retimes_menu = nuke.menu('Nuke').addMenu('Combine Retimes')" # Adds a Combine Retimes entry to the 'Nuke' menu.
            "combine_retimes_menu.addCommand('Combine Retimes', 'import combine_retimes')"

"""


import math
import nuke
import nukescripts


def count_node_inputs_recursive(node):
# Count the total number of parents that a node has (all the way back to the last parent in the node tree).

    number_inputs = 0

    for i in range(0, node.inputs()):

        if node.Class() == "Dissolve" and i == 2: # Avoid masks inputs for Dissolve and Kronos.
            continue
        elif node.Class() == "Kronos" and i != 0:
            continue

        node_input = node.input(i)

        if node_input:
            if node_input['selected'].value():

                # Launch recursive function, which iterates through all the node's inputs.
                # While adding +1 to number of inputs count.
                number_inputs += count_node_inputs_recursive(node_input) + 1

            else:
                continue
        else:
            continue

    return number_inputs


def check_selection(selected_nodes, valid_classes):

    invalid_class = False
    input_frame_range = [int(nuke.root()["first_frame"].value()), int(nuke.root()["last_frame"].value())]
    parents_dict = {}
    nodes_inputs_dict = {}
    accepted_knobs = ["timingFrame2", "lookup"]

    for node in selected_nodes:
        if node.Class() in valid_classes:

            # Get first frame, last frame from node.
            input_frame_range.append(node.firstFrame())
            input_frame_range.append(node.lastFrame())

            # Get all frames from existing keyframes and value from accepted knobs only.
            for knob in node.allKnobs():
                knob = knob.name()
                if node[knob].isAnimated():
                    all_curves = node[knob].animations()  # All curves in the knob.
                    for index in range(0, len(all_curves)):
                        curve = all_curves[index]
                        for key in curve.keys():
                            input_frame_range.append(int(key.x)) # Add keyframe.
                            if node[knob].name() in accepted_knobs:
                                input_frame_range.append(int(key.y))  # Add value.

            # Write all the nodes that are parents into a dictionary (later used to find out unplugged)
            for i in range(0, node.inputs() + 1):
                if node.input(i):
                    parent = node.input(i)
                    if parent.isSelected():
                        parents_dict[parent] = ""

            # Recursive function to iterate through the node's inputs, to sort them in order.
            number_inputs = count_node_inputs_recursive(node)
            nodes_inputs_dict[node] = number_inputs  # Add key (node) and value (number of parents).

        else:
            invalid_class = True
            return invalid_class, None, None, None, None # Only returning invalid class.

    input_frame_range = list(set(input_frame_range)) # Remove duplicates.
    input_frame_range.sort()

    sorted_nodes = sorted(nodes_inputs_dict, key=nodes_inputs_dict.get) # Sort order of nodes by number of parents (value).

    output_frame_range = [sorted_nodes[0].firstFrame(), sorted_nodes[-1].lastFrame()]

    return invalid_class, input_frame_range, sorted_nodes, parents_dict, output_frame_range


def panel(input_frame_range, output_frame_range):

    panel = nukescripts.PythonPanel("Combine Retimes")

    txt = nuke.Text_Knob("info", "", "<b>Please, confirm the assessed frame ranges:</b>")
    blank01 = nuke.Text_Knob("blank01", "", " ")

    input_txt = nuke.Text_Knob("input_txt", " Input: ", " ")
    input_first_frame = nuke.Int_Knob("input_first_frame", "")
    input_first_frame.setValue(min(input_frame_range))
    input_first_frame.clearFlag(nuke.STARTLINE)
    input_last_frame = nuke.Int_Knob("input_last_frame", "")
    input_last_frame.setValue(max(input_frame_range))
    input_last_frame.clearFlag(nuke.STARTLINE)

    output_txt = nuke.Text_Knob("framerange", "Ouput: ", " ")
    output_first_frame = nuke.Int_Knob("output_first_frame", "")
    output_first_frame.setValue(min(output_frame_range))
    output_first_frame.clearFlag(nuke.STARTLINE)
    output_last_frame = nuke.Int_Knob("output_last_frame", "")
    output_last_frame.setValue(max(output_frame_range))
    output_last_frame.clearFlag(nuke.STARTLINE)

    blank02 = nuke.Text_Knob("blank01", "", " ")
    divider = nuke.Text_Knob("divider", "")
    author = nuke.Text_Knob("author", "", "Author: Guillermo Algora")
    version = nuke.Text_Knob("version", "", "v1.0")
    blank03 = nuke.Text_Knob("blank02", "", " ")

    for knob in (txt, blank01, input_txt, input_first_frame, input_last_frame, output_txt, output_first_frame,
                 output_last_frame, blank02, divider, author, version, blank03):
        panel.addKnob(knob)

    while True:
        if panel.showModalDialog(): #If OK button.
            first_frame = input_first_frame.value()
            last_frame = input_last_frame.value() + 1 # To avoid -1 in ranges.
            output_first_frame = output_first_frame.value()
            output_last_frame = output_last_frame.value()
            return first_frame, last_frame, output_first_frame, output_last_frame
        else: #If Cancel button.
            raise StopIteration("Cancelled")


def create_frame_container():

    frame_container = nuke.createNode("Constant", inpanel=False)
    frame_container["postage_stamp"].setValue(False)

    crop = nuke.createNode("Crop", inpanel=False)
    crop["preset"].setValue("square"); crop["reformat"].setValue(True)
    crop["box"].setValue(0, 0)
    crop["box"].setValue(0, 1)
    crop["box"].setValue(3, 2)
    crop["box"].setValue(3, 3)

    return frame_container, crop

def prepare_nodes():

    # Copy the retime nodes.
    nuke.nodeCopy("%clipboard%")

    # Initialize group and create assist nodes.
    group = nuke.createNode("Group", inpanel=False)
    group["name"].setValue("Processing")
    group.begin()

    frame_container, crop = create_frame_container()
    frame_container["color"].setExpression("frame")

    curve_tool = nuke.createNode("CurveTool", inpanel=False)
    curve_tool["operation"].setValue("Avg Intensities")

    # Paste the retime nodes after the frame container.
    nukescripts.clear_selection_recursive()
    crop.setSelected(True)
    nuke.nodePaste("%clipboard%")

    return group, frame_container, curve_tool


def execute_curve_tool(curve_tool, first_frame, last_frame):

    try:
        nuke.execute(curve_tool, first_frame, last_frame)
    except Exception as e:  # Cancellation of the Curve Tool.
        print(str(e))
        stop = True
        return stop


def prepare_timewarps(node, curve_tool, stop):
    # Check for TimeWarps: they require pre-baking to adjust the values to the filter type.

    node = nuke.toNode("{}".format(node.name())) # We are inside the group now, so assigning the new nodes is required.

    if node.Class() == "TimeWarp":
        if node["filter"].value() != "box":  # If filter type is not 'box'.

            nukescripts.clear_selection_recursive()
            frame_container_alt, crop_alt = create_frame_container()
            frame_container_alt["color"].setAnimated()

            last_node = curve_tool.input(0)
            curve_tool.setInput(0, node)

            stop = execute_curve_tool(curve_tool, first_frame, last_frame)
            if stop:
                return stop

            for frame in range(first_frame, last_frame):

                value = curve_tool["intensitydata"].valueAt(frame, 0)

                if node["filter"].value() == "none":  # If 'none'.
                    value = math.floor(value)

                else:  # If 'nearest'.
                    value = round(value)

                frame_container_alt["color"].setValueAt(value, frame)

            nukescripts.clear_selection_recursive()
            node.setSelected(True)
            dot = nuke.createNode("Dot", inpanel=False)
            dot.setInput(0, crop_alt)
            curve_tool.setInput(0, last_node)

    return stop

def create_output_node():

    # Using nuke.nodes instead of nuke.CreateNode() does not raise an error with duplicated names.
    output_node = nuke.nodes.NoOp(name="CombinedRetime1")
    lookup = nuke.Double_Knob("lookup", "input frame")
    speed = nuke.Double_Knob("speed", "speed")
    for knob in (lookup, speed):
        output_node.addKnob(knob)
        output_node[knob.name()].setAnimated()

    return output_node


def auto_rename(node):

    nukescripts.clear_selection_recursive()
    node.setSelected(True)
    nuke.nodeCopy("%clipboard%")
    nuke.delete(node)
    nuke.nodePaste("%clipboard%")
    node = nuke.selectedNode()

    return node


def output_lookup(curve_tool, frame, output_node):

    output_node["lookup"].setValueAt(curve_tool["intensitydata"].valueAt(frame, 0), frame)


def output_speed(curve_tool, frame, first_frame, output_node):

    lookup = round(curve_tool["intensitydata"].valueAt(frame, 0))
    offset = abs(first_frame - 0.5)
    value = (lookup - offset) / (frame - offset)
    output_node["speed"].setValueAt(value, frame)


            ### EXECUTING APPLICATION ###

valid_classes = ["OFlow2", "TimeOffset", "FrameHold", "Retime", "TimeWarp", "Kronos", "Switch", "Dot", "Dissolve"]
selected_nodes = nuke.selectedNodes()

# STOP EXECUTION if no nodes are selected, invalid classes or unplugged.

def combineRetimes():
    if len(selected_nodes) == 0:
        nuke.message("You must select at least one node.")

    else:

        invalid_class, input_frame_range, sorted_nodes, parents_dict, output_frame_range = check_selection(selected_nodes, valid_classes)

        if invalid_class:
            nuke.message("At least one of the selected nodes\n"
                         "does not correspond with the following supported classes:\n\n"
                         + ", ".join(valid_classes) + ".")

        elif len(parents_dict) + 1 != len(selected_nodes): # If number of parents + 1 not equal selected nodes, some are unplugged.

            msg = ("At least one of the selected nodes is detached\n"
                   "from the others, please have them in a chain.")

            if nuke.env['nc']:
                nc_msg = ("* If running in Nuke Non-Commercial,\n"
                          "there is also the possibility that the 10 node limit for Node objects\n"
                          "accessible in Python has been reached. To debug, restart Nuke.")

                msg = "{}\n\n{}".format(msg, nc_msg)

            nuke.message(msg)


        # Else, PROCEED WITH THE APPLICATION:

        else:

            # Panel:
            first_frame, last_frame, output_first_frame, output_last_frame = panel(input_frame_range, output_frame_range)

            # After Panel:
            nuke.Undo.disable()
            stop = False
            progress_bar = nuke.ProgressTask("")

            try:

                # PREPARE ASSIST NODES:
                group, frame_container, curve_tool = prepare_nodes()

                for i, node in enumerate(sorted_nodes):
                    if not stop and not progress_bar.isCancelled():
                        progress_bar.setMessage("Preparing " + node.name())
                        progress_bar.setProgress(int((50 / len(sorted_nodes)) * (i+1)))
                        stop = prepare_timewarps(node, curve_tool, stop)

                group.end()

                # ANALYZE OUTPUT:
                if not stop and not progress_bar.isCancelled():
                    progress_bar.setMessage("Analyzing")
                    stop = execute_curve_tool(curve_tool, first_frame, last_frame)

                # OUTPUT RESULTS:
                if not stop and not progress_bar.isCancelled():
                    output_node = create_output_node()
                    output_node = auto_rename(node = output_node)
                    progress_bar.setMessage("Outputting")

                    for frame in range(output_first_frame, output_last_frame + 1): # To avoid -1 in range.
                        progress_bar.setProgress(int(75 + (float(frame + 1 - output_first_frame) / float(output_last_frame - output_first_frame) * 25)))
                        output_lookup(curve_tool, frame, output_node)
                        output_speed(curve_tool, frame, first_frame, output_node)
                else:
                    if progress_bar.isCancelled():
                        print("Cancelled")

            # WRAP UP
            finally:
                try:
                    group.end()
                    nuke.delete(group)
                    del progress_bar

                    # Enable undo for output node.
                    nuke.nodeCopy("%clipboard%")
                    nuke.delete(output_node)
                    nuke.Undo.enable()
                    nuke.nodePaste("%clipboard%")

                except:
                    pass