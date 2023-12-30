"""
DEVELOPER: Tor Andreassen - www.fxtor.net
DATE: Feb 28, 2022
VERSION: v1.3


DESCRIPTION:
    Clones are a nice feature in Nuke, but the random bug that comes with clones can corrupt your nuke script
    The Foundry claim the bug doesn't exist anymore. However, multiple artists have reported otherwise.
    It seems likely the bug has at some point been removed but accidentally introduced again in some versions of Nuke.
    This makes it risky to use clones, as one can't know if the bug still exists or if it could unintentionally be
    brought back in future versions of Nuke.
    
    This script makes it safe to use clones again by swapping it out with expressions.
    This script will let you set expressions on all knobs as if it was a clone, the only difference is that you will
    have a parent and child node in stead on the non-directional functionality of the clone, but you can be sure that
    your Nuke script will not randomly at some point become corrupted due to clones.

Features:
    - remove original clone from the menu and replace it with this tool (same placement in the menu and same shortcuts)
    Shortcuts are: Alt+K  or Alt+Shift+K (see USAGE below for how to add these shortcuts)

    - script allows you to clone and declone, just like the native clone feature

    - takes account for index on color knobs (grade and colorCorrect nodes is forced to multiValue knobs)
    This is restored to singleValue/original state of node when decloning

    - link all visible knobs, not linking hidden knobs, callback knobs or any other knobs that should not be linked

    - Links all selected nodes (you can select multiple nodes and link them at the same time)

    - won't let you link nodes that are considered unsafe to link (by Class or name of node),
    or groups (similar to the native nuke clone feature)

    - won't link the 'disable-knob' (toggling the 'disable-knob' by pressing 'd' will set animation on the knob if
    it's linked, so it's therefore not linkable by this tool).

Known drawbacks:
      - shuffle node links the dropdown menus, but the checkboxes don't link,
      lets not speak of the new shuffle nodes. (might look into this in the feature, atm. I would never link a shuffle)

USAGE:
    copy this file into your .nuke directory and make sure you can access the location of this file in the init file

    example:

    put this in your init.py file:
        nuke.pluginAddPath('./fxT_tools/fxT_cloneViaExpressions')

    put this in your menu.py file:  (PS: this removes access to the original clone node)

        # replace clone in meny with fxT_cloneViaExpressions
        import fxT_cloneViaExpressions
        nuke.menu('Nuke').addCommand('Edit/cloneViaExpression', 'fxT_cloneViaExpressions.clone_via_expression()','Alt+K', index=13)
        nuke.menu('Nuke').addCommand('Edit/DecloneExpression', 'fxT_cloneViaExpressions.clear_expression()', 'Alt+Shift+K', index=14)

        # remove original clone entries from the nuke menu
        edit_menu = menubar.findItem('&Edit')
        edit_menu.removeItem("Clone")
        edit_menu.removeItem("Declone")
        edit_menu.removeItem("Copy As Clones")
        edit_menu.removeItem("Force Clone")
"""

import nuke
import fnmatch


def clone_via_expression():
    if len(nuke.selectedNodes()) >= 1:

        # reset list every time tool is stored to assure correct nodes are listed
        # then generate list of selected nodes not containing pyScript_Knobs
        selection_list = []
        py_knob_list = []
        deny_nodes = []

        # make list of nodes to link via expressions
        for i in nuke.selectedNodes():
            selection_list.append(i.name())

            # might not be super smart, investigate nodes more
            if nuke.toNode(i.name()).Class() != 'ColorLookup':
                for x in i.knobs():
                    if nuke.toNode(i.name()).knob(x).Class() == 'PyScript_Knob':
                        py_knob_list.append(i.name())
        clone_list = list(set(selection_list) - set(py_knob_list))
        py_knob_list = list(set(py_knob_list))
        py_knob_list.sort()
        py_knob_list_string = '\n'.join(py_knob_list)

        # deselect all nodes
        for i in nuke.allNodes():
            i.setSelected(False)

        for node in clone_list:
            # make list of all node classes that are not wise to link
            # the * accounts for any version of the Class
            unwise_nodes = ['Group', 'Viewer*', 'Primatte*', 'Roto*', 'RotoPaint*',
                            'LightWrap*', 'VectorToMotion*', 'OFXuk.co.thefoundry.furnace.f*']

            # deny unwise node classes to be linked
            if any(fnmatch.fnmatch(nuke.toNode(node).Class(), x) for x in unwise_nodes):
                deny_nodes.append(nuke.toNode(node).name())

            # duplicate/placement/linking of nodes
            else:
                x = nuke.toNode(node).xpos()
                y = nuke.toNode(node).ypos()
                nuke.toNode(node).setSelected(True)
                nuke.nodeCopy('%clipboard%')
                nuke.toNode(node).setSelected(False)  # deselect parent node so the clone node is kept out of any stack
                clone_node = nuke.nodePaste('%clipboard%')
                try:
                    clone_node.removeKnob(clone_node.knob('clone_via_expression_cloneList'))
                    clone_node.removeKnob(clone_node.knob('clone_list'))
                    # force delete knobChanged as it is set on specific nodes to have curves knobs work correctly
                    clone_node.knob('knobChanged').setValue("")
                except:
                    pass
                nuke.selectedNode().setXYpos(x + 110, y + 20)
                # set a label on the clone_node (expression linked node) so you know where the link is coming from
                clone_node['label'].setValue('linked to: ' + node)

                # set onDestroy callback on clone_node if it can be part of the master_nodes knobChanged callback
                # (only for nodes with curve knobs) this is to update the callback on the master_node if nodes
                # are deleted so no callback is left if it's not needed.
                kill_code = "def update_master_clone_list():" \
                            "\n\tn = nuke.thisNode().dependencies(nuke.EXPRESSIONS)[0].name()" \
                            "\n\tclonelist = (nuke.toNode(n)." \
                            "knob('clone_via_expression_cloneList').value()).split(',')" \
                            "\n\tclonelist = [x for x in clonelist if x]" \
                            "\n\ttry:" \
                            "\n\t\tclonelist.remove(nuke.thisNode().name())" \
                            "\n\texcept ValueError:" \
                            "\n\t\tpass" \
                            "\n\tclonelist_str = ','.join(clonelist)" \
                            "\n\tnuke.toNode(n).knob('clone_via_expression_cloneList').setValue(clonelist_str)" \
                            "\n\tif (len(clonelist)) == 0:" \
                            "\n\t\ttry:" \
                            "\n\t\t\tnuke.toNode(n).removeKnob(nuke.toNode(n).knobs()" \
                            "['clone_via_expression_cloneList'])" \
                            "\n\t\t\tnuke.toNode(n).removeKnob(nuke.toNode(n).knobs()['clone_list'])" \
                            "\n\t\texcept ValueError:\n\t\t\tpass\nupdate_master_clone_list()"

                try:
                    if clone_node.Class() == 'HueCorrect' or clone_node.Class() == 'ColorCorrect' or \
                            clone_node.Class() == 'ScannedGrain' or clone_node.Class() == 'ColorLookup' or \
                            clone_node.Class() == 'HueKeyer' or clone_node.Class() == 'Sampler':
                        nuke.toNode(clone_node.name()).knob('onDestroy').setValue(kill_code)
                except:
                    pass

                # make sure grade/cc knobs (that have  3 or 4 indexes) are changed from singleValue to multiValue knobs
                # before linking them, this way if parent node change after it's been linked (from single to multiValue)
                # it will still link correctly, if the clone_node had a single value before linking it would not pick up
                # changes to a multiValue. it might technically work without those, but visually you won't be able to
                # see that it's working correctly unless this multiValue is set.

                for i in clone_node.knobs():
                    if clone_node[i].Class() == 'Color_Knob':
                        val = bool(clone_node[i].value())
                        clone_node[i].setValue([val, val, val])
                    elif clone_node[i].Class() == 'AColor_Knob':
                        val = bool(clone_node[i].value())
                        clone_node[i].setValue([val, val, val, val])
                    elif clone_node[i].Class() == 'WH_Knob':
                        val = bool(clone_node[i].value())
                        clone_node[i].setValue([val, val])
                    else:
                        pass

                clone_node.setSelected(False)
                # find all hidden knobs (they should not be linked)
                hidden_knobs = []
                string_knobs = []
                for i in nuke.toNode(node).knobs():
                    if nuke.toNode(node).knob(i).getFlag(0x00000400):
                        hidden_knobs.append(i)
                    if isinstance(nuke.toNode(node).knob(i), nuke.String_Knob):
                        string_knobs.append(i)

                # make list ignore-knobs (hidden knobs + set of default knobs that should never be linked)
                ignore_knobs = ['lifetimeEnd', 'note_font_color', 'note_font', 'bookmark', 'dope_sheet', 'label',
                                'hide_input', 'postage_stamp_frame', 'lifetimeStart', 'cached', 'note_font_size',
                                'useLifetime', 'postage_stamp', 'Obsolete_Knob', 'PyScript_Knob', 'Tab_Knob',
                                'Script_Knob', 'Text_Knob', 'Transform2d_Knob', 'snap_menu', 'file_menu', 'reload',
                                'disable']
                ignore_knobs = ignore_knobs + hidden_knobs
                ignore_knobs = list(dict.fromkeys(ignore_knobs))

                parent_node_knobs = list(set(nuke.toNode(node).knobs()) - set(ignore_knobs))
                clone_node_knobs = list(set(clone_node.knobs()) - set(ignore_knobs))

                # set callbacks on master_node that is linked to nodes that have curves in them
                # (they can't be linked, callbacks sort this, so they act as if they were linked)
                # decide knob curve_type
                curve_type = ''  # initialize variable
                reset_knob = 'channels'  # this variable is used to set focus on the first tab
                if node.startswith('HueCorrect'):
                    curve_type = 'hue'
                elif node.startswith('ColorCorrect'):
                    curve_type = 'lookup'
                elif node.startswith('ScannedGrain'):
                    curve_type = 'weight'
                    reset_knob = 'mix'
                elif node.startswith('ColorLookup') or node.startswith('HueKeyer') or node.startswith('Sampler'):
                    curve_type = 'lut'

                # sampler node have the option to sample the current frame, this won't update the lut before the
                # lut knob is triggered (so technically it's not a true clone but close enough)
                if node.startswith('HueCorrect') or node.startswith('ColorCorrect') or node.startswith('HueKeyer') or \
                        node.startswith('ColorLookup') or node.startswith('ScannedGrain') or node.startswith('Sampler'):

                    if not nuke.toNode(node).knob('clone_via_expression_cloneList'):
                        nuke.toNode(node).addKnob(nuke.Tab_Knob('clone_list'))
                        nuke.toNode(node).addKnob(nuke.String_Knob('clone_via_expression_cloneList', 'clone_list', ''))
                        nuke.toNode(node).knob('clone_via_expression_cloneList').setValue(clone_node.name())
                        nuke.toNode(node)[reset_knob].setFlag(0)  # set focus on the first tab

                    curr_clones = nuke.toNode(node).knob('clone_via_expression_cloneList').value().split(",")
                    curr_clones.append(clone_node.name())
                    curr_clones = [x for x in curr_clones if x]  # remove blanks
                    curr_clones = set(curr_clones)
                    curr_clones = list(curr_clones)
                    curr_clones.sort()

                    # delete non existent nodes
                    none_existent_clones = []
                    for i in curr_clones:
                        if not nuke.toNode(i):
                            none_existent_clones.append(i)

                    curr_clones = [x for x in curr_clones if (x not in none_existent_clones)]
                    curr_clones = ",".join(curr_clones)

                    nuke.toNode(node).knob('clone_via_expression_cloneList').setValue(curr_clones)

                    # make list of nodes
                    clone_list = nuke.toNode(node).knob('clone_via_expression_cloneList').value().split(',')
                    my_code = "def curveClone():\n\tif nuke.thisKnob().name() =='" + curve_type + "':\n\t\ttry:"
                    for i in clone_list:
                        my_code = my_code + "\n\t\t\tnuke.toNode(" + "'" + i + "'" + ")['" + curve_type + "'].fromScript(nuke.thisKnob().toScript())"
                    my_code = my_code + "\n\t\texcept:\n\t\t\tpass\ncurveClone()"
                    nuke.toNode(node).knob('knobChanged').setValue(my_code)

                # deselect clone nodes
                clone_node.setSelected(False)

                # linking of knobs
                for pnk in parent_node_knobs:
                    for cnk in clone_node_knobs:
                        if cnk == pnk:
                            for ink in ignore_knobs:
                                if cnk != ink:
                                    if cnk == 'channel':
                                        clone_node.knob(cnk).setExpression(
                                            'parent.%s' % nuke.toNode(node).knob('name').value() + '.%s' % 'channels')
                                    elif cnk == 'mask':
                                        clone_node.knob(cnk).setExpression('parent.%s' % nuke.toNode(node).knob(
                                            'name').value() + '.%s' % 'maskChannelInput')

                                    elif cnk == 'use_precomputed' and clone_node.Class() == 'ColorLookup':
                                        clone_node.knob(cnk).clearAnimated()

                                    elif cnk in string_knobs:
                                        clone_node.knob(cnk).setValue(
                                            "[value %s.%s]" % (nuke.toNode(node).knob('name').value(), pnk))

                                    else:
                                        clone_node.knob(cnk).setExpression(
                                            'parent.%s' % nuke.toNode(node).knob('name').value() + '.%s' % pnk)

        deny_nodes_string = '\n'.join(deny_nodes)
        # show warning about not linking selected nodes with pyScipt_Knobs on it
        if len(py_knob_list) > 0 and len(deny_nodes) > 0:
            nuke.message('The selected nodes contains pyScriptButton or is otherwise unwise to link.'
                         'Linking was bypassed for these nodes:\n\n\n' + py_knob_list_string + "\n\n" + deny_nodes_string)
        elif len(py_knob_list) > 0:
            nuke.message('The selected nodes contain pyScriptButton and should not be linked.'
                         ' linking bypassed for these nodes:\n\n\n' + py_knob_list_string)
        elif len(deny_nodes) > 0:
            nuke.message("It's unwise to link nodes of the selected type. Linking was bypassed for these nodes:"
                         "\n\n\n" + deny_nodes_string)
        else:
            pass

    # this is saying what happens if no nodes are selected.
    elif len(nuke.selectedNodes()) == 0:
        pass  # could display no nodes selected, but choosing to not annoy the user with this


def clear_expression():
    if len(nuke.selectedNodes()) >= 1:

        clear_expr_list = []
        string_knobs = []
        hidden_knobs = []
        special_knob = ['ChannelMask_Knob', 'ChannelSet_knob', 'Channel_Knob']

        # make list of nodes to link via expressions
        for i in nuke.selectedNodes():
            for x in i.knobs():
                if nuke.toNode(i.name())[x].Class() in special_knob:
                    clear_expr_list.append(x)
                if isinstance(nuke.toNode(i.name()).knob(x), nuke.String_Knob):
                    string_knobs.append(x)
                if nuke.toNode(i.name())[x].getFlag(0x00000400):
                    hidden_knobs.append(x)

        # add curve knobs to the clear expression knob-list
        clear_expr_list.append('hue')
        clear_expr_list.append('lookup')
        clear_expr_list.append('weight')
        clear_expr_list.append('lut')

        clear_expr_list = list(set(clear_expr_list))
        clear_expr_list.sort()

        for node in nuke.selectedNodes():

            # this gives you a list of the master nodes:
            # this is where you remove from list and kill the callback if it exists.
            try:
                for i in node.dependencies(nuke.EXPRESSIONS):
                    master_node = i.name()

                if nuke.toNode(master_node).Class() in ['HueCorrect', 'ColorCorrect', 'HueKeyer', 'ColorLookup', 'ScannedGrain', 'Sampler']:

                    # decide knob curve_type for callback rebuild
                    curve_type = ''  # initialize variable
                    if master_node.startswith('HueCorrect'):
                        curve_type = 'hue'
                    elif master_node.startswith('ColorCorrect'):
                        curve_type = 'lookup'
                    elif master_node.startswith('ScannedGrain'):
                        curve_type = 'weight'
                    elif master_node.startswith('ColorLookup') or master_node.startswith(
                            'HueKeyer') or master_node.startswith('Sampler'):
                        curve_type = 'lut'

                    clone_list = nuke.toNode(master_node).knob('clone_via_expression_cloneList').value().split(',')
                    clone_list = [x for x in clone_list if x]  # remove blanks
                    clone_list.remove(node.name())  # remove
                    clone_list = set(clone_list)  # remove duplicates
                    clone_list = list(clone_list)  # back to list

                    # delete non-existent nodes
                    non_existent = []
                    for i in clone_list:
                        if not nuke.toNode(i):
                            non_existent.append(i)

                    clone_list = [x for x in clone_list if (x not in non_existent)]
                    clone_list.sort()

                    clone_list = ",".join(clone_list)

                    nuke.toNode(master_node).knob('clone_via_expression_cloneList').setValue(clone_list)

                    # make list of nodes still linked, update callback to right amount of cloneNodes
                    clone_list2 = nuke.toNode(master_node).knob('clone_via_expression_cloneList').value().split(',')
                    my_code2 = "def curveClone():\n\tif nuke.thisKnob().name() =='" + curve_type + "':\n\t\ttry:"
                    for i in clone_list2:
                        my_code2 = my_code2 + "\n\t\t\tnuke.toNode(" + "'" + i + "'" + ")['" + curve_type + "'].fromScript(nuke.thisKnob().toScript())"
                    my_code2 = my_code2 + "\n\t\texcept:\n\t\t\tpass\ncurveClone()"

                    if i == '' or i is None:
                        nuke.toNode(master_node).knob('knobChanged').setValue('')
                        nuke.toNode(master_node).removeKnob(
                            nuke.toNode(master_node).knob('clone_via_expression_cloneList'))
                        nuke.toNode(master_node).removeKnob(nuke.toNode(master_node).knob('clone_list'))
                    else:
                        nuke.toNode(master_node).knob('knobChanged').setValue(my_code2)

            except:
                pass

            for y in node.knobs():
                node[y].setEnabled(True)

                if y in clear_expr_list:
                    node[y].setExpression('')  # just remove the expression

                if y in string_knobs and y not in hidden_knobs:
                    try:
                        string_bake_value = nuke.toNode(master_node).knob(y).value()
                        node.knob(y).setValue(string_bake_value)
                    except:
                        node.knob(y).setValue('')

                # when decloning restore curve knob values and remove onDestroy and knobChanged from node
                if y in ['hue', 'lookup', 'weight', 'lut']:

                    # reset curves after decloning
                    try:
                        node.knob(curve_type).fromScript(nuke.toNode(master_node).knob(curve_type).toScript())
                        node.knob('onDestroy').setValue('')
                        node.knob('knobChanged').setValue('')
                    except AttributeError:
                        nuke.message('please only declone nodes from the same class at the same time')
                        return

                else:
                    node.knob(y).clearAnimated()

            # set label to parentnode label, if fail set label to blank or its own label (don't change non-linked nodes)
            try:
                node['label'].setValue(nuke.toNode(master_node)['label'].value())
            except:
                if node.knob('label').value().startswith('linked to:'):
                    node.knob('label').setValue('')
                else:
                    pass

        # set single values on knobs if the same value is present in all knobs on multiIndex knobs (hack to bring back
        # grade/cc nodes to its original singleValue state before it was linked with the clone_via_expressions script)
        sel_nodes = []
        for x in nuke.selectedNodes():
            sel_nodes.append(x.name())

        for i in sel_nodes:
            for k in nuke.toNode(i).knobs():
                if nuke.toNode(i).knob(k).Class() == 'Color_Knob' or nuke.toNode(i).knob(k).Class() == 'AColor_Knob' or \
                        nuke.toNode(i).knob(k).Class() == 'WH_Knob':
                    try:
                        knob_list = nuke.toNode(i).knob(k).value()
                        knob_list = set(knob_list)
                        knob_list = list(knob_list)
                        num = ' '.join([str(elem) for elem in knob_list])
                        num = float(num)
                        nuke.toNode(i).knob(k).setValue(num)
                    except:
                        pass

    # this is saying what happens if no nodes are selected.
    elif len(nuke.selectedNodes()) == 0:
        pass  # could display no nodes selected, but choosing to not annoy the user with this
