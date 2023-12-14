

"""

new_ref_frame.py
Version: 1.2.0
Author: Guillermo Algora
Last Updated: Aug 12th, 2021

This tool will help you to:
A) Set a new reference frame for any Transform or CornerPin2D node.
B) Generate data for MatchMove or Stabilize.

Usage:
- Select a Transform or CornerPin2D node.
- From the Panel:
   - Select origin node function.
   - Select new node function.
   - Enter new reference frame.


This script is executable directly from Nuke's Script Editor.

Installation:
  1) Place 'new_ref_frame.py' in a directory that is part of the Nuke plugin path (to find out these directories
                                                                                   execute: "nuke.pluginPath()").

  2) In a 'menu.py' file: choose a menu and add the command "import new_ref_frame".   

     e.g. (will create a new menu for 'New Ref Frame' and add the command necessary).
        menu.py, add:
            "new_ref_frame_menu = nuke.menu('Nuke').addMenu('New Ref Frame')"
            "new_ref_frame_menu.addCommand('New Ref Frame', 'import new_ref_frame')"

"""


# # # # # # # # CORE # # # # # # # #


import nuke
import threading
import nukescripts
import math


def check_selection():

    # LETS CHECK SELECTED NODES:

    # Check the amount of selected Nodes:
    nodes = len([n.name() for n in nuke.selectedNodes()])

    if nodes > 1:
        nuke.message('\n"New Reference Frame" requires a single node to be selected.')
        return

    if nodes == 0:
        try:
            nc = nuke.env['nc']
        except:
            pass

        nodes_text = ('\n"New Reference Frame" requires one'
                      "\n'Transform' or 'CornerPin2D' node to be selected.")

        if nc:
            nc_text = ("* If one node is selected and running in Nuke Non-Commercial:"
                       "\nPossibly, the 10-node limit for Node objects accessible in Python"
                       "\nhas been reached. To debug, restart Nuke.")

            nuke.message(nodes_text + "\n\n" + nc_text + "\n")
            return

        else:
            nuke.message(nodes_text)
            return

    # One Node is selected:
    origin_node = nuke.selectedNodes()[0]

    # Check the Class of selected Node: Two different dictionaries:
    is_transform = False

    if origin_node.Class() == 'Transform':

        is_transform = True

        knobs_dic = {"translate": ["translate", nuke.XY_Knob],
                     "rotate": ["rotate", nuke.Double_Knob],
                     "scale": ["scale", nuke.WH_Knob],
                     "skewX": ["skewX", nuke.Double_Knob],
                     "skewY": ["skewY", nuke.Double_Knob],
                     "center": ["center", nuke.XY_Knob]}

        extra_knobs_dic = {"skew_order": ["skew_order", nuke.Enumeration_Knob],
                           "filter": ["filter", nuke.Enumeration_Knob],
                           "black_outside": ["black_outside", nuke.Boolean_Knob],
                           "motionblur": ["motionblur", nuke.Array_Knob]}

    elif origin_node.Class() == 'CornerPin2D':

        knobs_dic = {"to1": ["to1", nuke.XY_Knob],
                     "to2": ["to2", nuke.XY_Knob],
                     "to3": ["to3", nuke.XY_Knob],
                     "to4": ["to4", nuke.XY_Knob]}

        extra_knobs_dic = {"enable1": ["enable1", nuke.Boolean_Knob],
                           "enable2": ["enable2", nuke.Boolean_Knob],
                           "enable3": ["enable3", nuke.Boolean_Knob],
                           "enable4": ["enable4", nuke.Boolean_Knob],
                           "filter": ["filter", nuke.Enumeration_Knob],
                           "black_outside": ["black_outside", nuke.Boolean_Knob]}

    else:  # If not "Transform" or "CornerPin"
        nuke.message("\nPlease select a suitable 'Transform' or 'CornerPin2D' node.")
        return

    # LETS CHECK IF SELECTED NODE HAS EXPRESSION OR INVERT:

    expression_warning = invert_warning = False
    expression_knobs_list = []

    for knob in origin_node.knobs():

        if origin_node[knob].hasExpression():
            knob_name = origin_node[knob].name()

            if knob_name in knobs_dic:
                knob_name = knob_name.capitalize()
                expression_knobs_list.append(knob_name)
                expression_warning = True

        if "invert" in origin_node[knob].name():

            if origin_node[knob].value() is True:
                invert_warning = True

    if expression_warning:
        expression_knobs_list = "{}".format(expression_knobs_list)
        expression_knobs_list = expression_knobs_list.replace("[", "")
        expression_knobs_list = expression_knobs_list.replace("]", ".")

        nuke.message("The following knobs have expressions:"
                     "\n" + expression_knobs_list +
                     "\n\nPlease, bake in the values first:"
                     "\nKnob (right-click) > Edit > Generate.")
        return

    if invert_warning:
        # Panel to ask user if to proceed:

        warning_panel = nukescripts.PythonPanel()

        text = ("'Invert' is activated in the origin Node:"
                "\n\nThe tool will OMIT this setting and perform functions"
                "\n from the values within the knobs."
                "\n\n* Careful attention to the origin Node function is advisable."
                "\n\nDo you wish to proceed?\n")

        warning_panel.addKnob(nuke.Text_Knob('warning_text', " ", text))

        while True:
            if warning_panel.showModalDialog():
                break
            else:
                return

    return origin_node, is_transform, knobs_dic, extra_knobs_dic

def panel_main():

    # Panel for Action & Frame Input. This function creates the Panel and executes it with execute_panel.

    # Create Panel
    panel = nukescripts.PythonPanel()

    from_enumeration = nuke.Enumeration_Knob('from', 'From: ', ['MatchMove', 'Stabilize'])
    from_enumeration.setTooltip("Select function of origin node.")

    to_enumeration = nuke.Enumeration_Knob('to', 'To: ', ['MatchMove', 'Stabilize'])
    to_enumeration.setTooltip("Select function of new node.")

    user_frame = nuke.String_Knob('user_frame', "New Ref. Frame: ")
    user_frame.setTooltip("Enter new reference frame.")

    blank_space1 = nuke.Text_Knob('blank_space1', '', " ")
    blank_space2 = nuke.Text_Knob('blank_space2', '', " ")

    multithread = nuke.Boolean_Knob('enable_multithread', "Enable Multi-threading ")
    multithread.setTooltip("Multi-threading results in fast processing but is less stable. Turn off if any issues.")

    divider = nuke.Text_Knob('divider', '', '')
    author = nuke.Text_Knob('author', "", "Author: Guillermo Algora")
    blank_space3 = nuke.Text_Knob('blank_space3', '', " ")

    for knob in (from_enumeration, to_enumeration, user_frame, blank_space1, blank_space2, multithread, divider, author, blank_space3):
        panel.addKnob(knob)

    multithread.setValue(True)

    frame_input = ""

    # Execute Panel (execute_panel)
    while not frame_input.isdigit():
        frame_input, m_to_m, m_to_s, s_to_s, s_to_m, multithread, cancel = execute_panel(panel, from_enumeration, to_enumeration, user_frame, multithread)
        if cancel:
            return

    frame_input = int(frame_input)

    return frame_input, m_to_m, m_to_s, s_to_s, s_to_m, multithread

def execute_panel(panel, from_enumeration, to_enumeration, user_frame, multithread):  # Get Action & Frame input

    m_to_m = m_to_s = s_to_s = s_to_m = cancel = False
    frame_input = None

    while True:
        if panel.showModalDialog():  # If "OK" button
            from_choice = from_enumeration.value()
            to_choice = to_enumeration.value()
            frame_input = user_frame.value()
            multithread = multithread.value()

            if frame_input is None:
                cancel = True
                break

            elif frame_input.isdigit():

                if from_choice == "MatchMove":
                    if from_choice == to_choice:
                        m_to_m = True
                    else:
                        m_to_s = True
                    break

                if from_choice == "Stabilize":
                    if from_choice == to_choice:
                        s_to_s = True
                    else:
                        s_to_m = True
                    break

            else:
                nuke.message("\nPlease insert a numerical new reference frame.")

        else:  # If "Cancel" button
            cancel = True
            break

    return frame_input, m_to_m, m_to_s, s_to_s, s_to_m, multithread, cancel


def frame_range(knobs_dic, origin_node, frame_input):
    frame_range_list = []

    for key in list(knobs_dic.keys()):
        target_knob = knobs_dic[key][0]

        if target_knob in origin_node.knobs():

            if origin_node[target_knob].isAnimated():

                for index in range(0, 2):

                    try:
                        animation_curve = origin_node[target_knob].animation(index)
                        for key in list(animation_curve.keys()):
                            frame = key.x
                            frame_range_list.append(int(frame))
                    except:
                        pass

    frame_range_list.append(int(frame_input))
    frame_range_list.sort()

    first_frame = frame_range_list[0]
    last_frame = frame_range_list[-1] + 1
    return first_frame, last_frame


def perform_zero_out(first_frame, last_frame, origin_node, new_node, multithread, knobs_dic, frame_input, m_to_m, m_to_s, s_to_s, s_to_m):
    invert_result = False
    if m_to_s or s_to_m:
        invert_result = True

    for key in list(knobs_dic.keys()):
        target_knob = knobs_dic[key][0]

        try:

            task = nuke.ProgressTask("Processing")
            task.setMessage("Processing: " + target_knob)

            # Code for Transform:
            if new_node.Class() == 'Transform':

                for frame in range(first_frame, last_frame):

                    if task.isCancelled():
                        if multithread:
                            nuke.executeInMainThread(nuke.message, args=("Cancelled"))
                        else:
                            nuke.message("\nCancelled")
                        del task
                        nuke.delete(new_node)
                        return  # Exit the function

                    try:
                        new_node[target_knob].setSingleValue(origin_node[target_knob].singleValue())
                    except:
                        pass

                    index_max = 1
                    if not origin_node[target_knob].singleValue():  # If single value not true, do index 1
                        index_max = 2

                    for index in range(0, index_max):

                        if "center" not in target_knob:  # For All, except Center:

                            if origin_node[target_knob].isAnimated(index):  # If animated:
                                new_node[target_knob].setAnimated(index)

                                new_node[target_knob].setKeyAt(frame_input, index)  # Force key at new reference frame

                                # If origin node has key at frame: set key in new node
                                if origin_node[target_knob].isKeyAt(frame, index):
                                    new_node[target_knob].setKeyAt(frame, index)

                                # After transferring the keys from origin node to new node + key at new ref. frame
                                if new_node[target_knob].isKeyAt(frame, index):

                                    # Lets apply new values:
                                    static_value = origin_node[target_knob].getValueAt(frame_input, index)
                                    value = origin_node[target_knob].getValueAt(frame, index)

                                    if "scale" in target_knob:  # For Scale
                                        result = value / static_value

                                        if invert_result:
                                            result = static_value / value

                                    else:  # For All the others
                                        result = value - static_value

                                        if invert_result:
                                            result = - result

                                    new_node[target_knob].setValueAt(result, frame, index)

                            else:  # If not animated, no need for new values:
                                new_node[target_knob].setValue(origin_node[target_knob].value(index), index)

                        else:  # For Center:

                            new_node[target_knob].setAnimated(index)
                            new_node[target_knob].setKeyAt(frame_input, index)  # Force key at new reference frame

                            if m_to_m:  # MatchMove to MatchMove
                                new_center = (origin_node['translate'].valueAt(frame_input, index)
                                              + origin_node['center'].valueAt(frame_input, index))

                                new_node[target_knob].setValueAt(new_center, frame_input, index)

                            if m_to_s:  # MatchMove to Stabilize
                                new_center = (origin_node['translate'].valueAt(frame, index)
                                              + origin_node['center'].valueAt(frame, index))

                                new_node[target_knob].setValueAt(new_center, frame, index)

                            if s_to_s:  # Stabilize to Stabilize
                                if origin_node[target_knob].isAnimated(index):
                                    new_node[target_knob].copyAnimation(index, origin_node[target_knob].animation(index))

                                else:
                                    new_node[target_knob].setValue(origin_node[target_knob].value(index), index)

                            if s_to_m:  # Stabilize to MatchMove
                                new_node[target_knob].setValueAt(origin_node[target_knob]
                                                                 .valueAt(frame_input, index), frame_input, index)

                    percentage = float(frame - first_frame) / float(last_frame - first_frame) * 100
                    task.setProgress(int(percentage))

            # Code for CornerPin2D:
            else:

                for index in range(0, 2):

                    if task.isCancelled():
                        if multithread:
                            nuke.executeInMainThread(nuke.message, args=("Cancelled"))
                        else:
                            nuke.message("\nCancelled")
                        del task
                        nuke.delete(new_node)
                        return  # Exit the function

                    # If animated: transfer animation from origin node to new node
                    # Else, transfer value
                    try:
                        if origin_node[target_knob].isAnimated(index):
                            new_node[target_knob].copyAnimation(index, origin_node[target_knob].animation(index))
                        else:
                            new_node[target_knob].setValue(origin_node[target_knob].value(index), index)
                    except:
                        pass

                    task.setProgress(50)

                    # Performing zero out to "From"
                    try:
                        new_node[target_knob.replace('to', 'from')].setValue(origin_node[target_knob]
                                                                             .valueAt(frame_input, index), index)
                    except:
                        pass

                    task.setProgress(100)

                if m_to_m or s_to_m:
                    new_node['invert'].setValue(False)

                if m_to_s or s_to_s:
                    new_node['invert'].setValue(True)

        except:
            raise


def check_values(origin_node, new_node, multithread, first_frame, last_frame, frame_input, m_to_m, m_to_s, s_to_s, s_to_m, knobs_dic):
    # Check if current values need compensation.

    task = nuke.ProgressTask("Verifying")
    task.setMessage("Verifying: translate")

    oc = nuke.OutputContext()

    for frame in range(first_frame, last_frame):

        if task.isCancelled():
            if multithread:
                nuke.executeInMainThread(nuke.message, args=("Cancelled"))
            else:
                nuke.message("\nCancelled")
            del task
            nuke.delete(new_node)
            return  # Exit the function

        oc.setFrame(frame)
        frame_matrix = origin_node['matrix'].value(oc)

        oc.setFrame(frame_input)
        frame_input_matrix = origin_node['matrix'].value(oc)

        # Operation to the matrix:

        if m_to_m:
            resulting_matrix = frame_matrix * frame_input_matrix.inverse()

        if m_to_s:
            resulting_matrix = frame_input_matrix * frame_matrix.inverse()

        if s_to_s:
            resulting_matrix = frame_input_matrix.inverse() * frame_matrix

        if s_to_m:
            resulting_matrix = frame_matrix.inverse() * frame_input_matrix

        new_center_x = new_node['center'].valueAt(frame, 0)
        new_center_y = new_node['center'].valueAt(frame, 1)

        vector = nuke.math.Vector3(new_center_x, new_center_y, 0)
        transformed_vector = resulting_matrix.transform(vector)

        translate_x = transformed_vector[0] - new_center_x
        translate_y = transformed_vector[1] - new_center_y

        # Matrix decomposition

        rm = resulting_matrix

        angle = math.atan2(rm[1], rm[0])
        denom = pow(rm[0], 2) + pow(rm[1], 2)
        delta = (rm[0] * rm[5]) - (rm[4] * rm[1])

        rotation = angle / (math.pi / 180)
        scale_x = math.sqrt(denom)
        scale_y = delta / scale_x
        skew_x = (rm[0] * rm[4] + rm[1] * rm[5]) / delta 

        # Check current values against updated values:

        for key in list(knobs_dic.keys()):
            target_knob = knobs_dic[key][0]      

            if "center" in target_knob or "skewY" in target_knob: # Omit center and skewY
                pass

            else:

                index_max = 1
                if "translate" in target_knob or "scale" in target_knob:
                    index_max = 2

                for index in range(0, index_max):

                    current_value = new_node[target_knob].valueAt(frame, index)

                    if "translate" in target_knob:

                        if index == 0:
                            updated_value = translate_x
                        else:
                            updated_value = translate_y

                    if "rotate" in target_knob:
                        updated_value = rotation

                    if "scale" in target_knob:

                        if index == 0:
                            updated_value = scale_x
                        else:
                            updated_value = scale_y

                    if "skewX" in target_knob:
                        updated_value = skew_x

                    current_value = float("{:0.3f}".format(current_value))
                    updated_value = float("{:0.3f}".format(updated_value))

                    difference = current_value - updated_value
                    difference = float("{:0.2f}".format(difference))

                    if abs(difference) > 0.005:

                        new_node[target_knob].setSingleValue(False)

                        new_node[target_knob].setAnimated(index)
                        new_node[target_knob].setValueAt(updated_value, frame, index)
                        
                        # If there is difference, as skewY is never solved, restore it to 0.
                        new_node["skewY"].clearAnimated()
                        new_node["skewY"].setValue(0)

        percentage = float(frame - first_frame) / float(last_frame - first_frame) * 100
        task.setProgress(int(percentage))


def check_center(new_node):
    # Check if center has a single key and remove animation.

    for index in range(0, 2):
        animation_curve = new_node["center"].animation(index)

        if len(animation_curve.keys()) == 1:
            new_node["center"].clearAnimated(index) 


def apply_extra_knobs(origin_node, new_node, extra_knobs_dic):
    # Lets transfer settings of "extra" knobs from origin node to new node
    for key in list(extra_knobs_dic.keys()):
        knob_name = extra_knobs_dic[key][0]

        if knob_name in origin_node.knobs():
            new_node[knob_name].setValue(origin_node[knob_name].value())


def label(new_node, frame_input, m_to_m, m_to_s, s_to_s, s_to_m):
    if m_to_m or s_to_m:
        function = "MatchMove"

    if m_to_s or s_to_s:
        function = "Stabilize"

    if not nuke.env['nc']:
        nodes_list = []
        for node in nuke.allNodes():
            if "{}".format(function) in node.name():
                store_digit = []

                for character in node.name():
                    if character.isdigit():
                        store_digit.append(character)
                
                store_digit = int("".join(store_digit))
                nodes_list.append(store_digit)

        nodes_list.append(0)
        nodes_list.sort()

        number = int(max(nodes_list)) + 1

        new_node['label'].setValue("Ref. frame: {}".format(frame_input))
        new_node['name'].setValue("{}_{}{}".format(new_node.Class(), function, number))

    else:  # If Non-Commercial
        new_node['label'].setValue(function + "\n" + "Ref. frame: {}".format(frame_input))
        try:
            new_node['name'].setFlag(0)
        except:
            pass


# # # # # # # # EXECUTE APP FUNCTION # # # # # # # #


def execute_app():

    # CREATE NEW NODE:

    origin_node.setSelected(False)

    if is_transform:
        new_node = nuke.createNode("Transform", inpanel=False)
        invert_status = origin_node['invert_matrix'].value()  # Save status of invert in origin node
        origin_node['invert_matrix'].setValue(False)  # Set Invert to false.

    else:
        new_node = nuke.createNode("CornerPin2D", inpanel=False)

    # Position new node:
    new_node.setXYpos(origin_node.xpos() + 50, origin_node.ypos() + 50)
    new_node.autoplace()

    # Restore selection
    origin_node.setSelected(True)
    new_node.setSelected(False)


    # EXECUTE: FRAME RANGE, PERFORM ZERO-OUT, APPLY EXTRA KNOBS & LABEL.

    try:
        first_frame, last_frame = frame_range(knobs_dic, origin_node, frame_input)

        if multithread:
            thread01 = threading.Thread(target=perform_zero_out, args=(first_frame, last_frame, origin_node, new_node, multithread, 
                                                                       knobs_dic, frame_input, m_to_m, m_to_s, s_to_s, s_to_m))
            thread01.start()
            thread01.join()
        else:
            perform_zero_out(first_frame, last_frame, origin_node, new_node, multithread, knobs_dic, frame_input, m_to_m, m_to_s, s_to_s, s_to_m)
    except:
        raise

    try:
        if multithread:
            thread02 = threading.Thread(target=apply_extra_knobs, args=(origin_node, new_node, extra_knobs_dic))
            thread02.start()

            thread03 = threading.Thread(target=label, args=(new_node, frame_input, m_to_m, m_to_s, s_to_s, s_to_m))
            thread03.start()
        else:
            apply_extra_knobs(origin_node, new_node, extra_knobs_dic)
            label(new_node, frame_input, m_to_m, m_to_s, s_to_s, s_to_m)
    except:
        pass

    finally:
        if is_transform:
            try:
                if multithread:
                    thread04 = threading.Thread(target=check_values, args=(origin_node, new_node, multithread, first_frame, last_frame,
                                                                              frame_input, m_to_m, m_to_s, s_to_s, s_to_m, knobs_dic))
                    thread04.start()
                    thread04.join()                  

                else:
                    check_values(origin_node, new_node, multithread, first_frame, last_frame, frame_input, m_to_m, m_to_s, s_to_s, s_to_m, knobs_dic)

                check_center(new_node)
                origin_node['invert_matrix'].setValue(invert_status)
            except:
                pass

    return


# # # # # # # # EXECUTE APP # # # # # # # #


origin_node, is_transform, knobs_dic, extra_knobs_dic = check_selection()
frame_input, m_to_m, m_to_s, s_to_s, s_to_m, multithread = panel_main()
execute_app()