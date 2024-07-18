#------------------------------------------------------------------------------

# $GUI Tool
# by Prasannakumar T Bhat
# This handle GUI expression.
# if scanlineRender is selected sets the expression for sample knob (hope nobody wants to disable this :P )
# for all other nodes it sets $gui expression for disable knob if exists
# if knobs already has any expression, it clears that.
# if no node is selected drops a gui Handler node to control the script

#------------------------------------------------------------------------------

def guiTool():
    selNodes = nuke.selectedNodes()

    if not selNodes:
        nuke.createNode("guiToolNode")
        # https://www.nukepedia.com/toolsets/other/gui-expression-finder
        return

    for sel in selNodes:
        has_gui_expression = False

        # Iterate through all knobs in the node
        for knob_name in sel.knobs():
            knob = sel[knob_name]
            try:
                knobwidth = knob.width()
            except AttributeError:
                knobwidth = 1

            # Check each channel of the knob for expressions
            for idx in range(knobwidth):
                if knob.hasExpression(idx):
                    knob_expr = knob.animation(idx).expression()
                    if '$gui' in knob_expr:
                        has_gui_expression = True
                        new_knob_expr = knob_expr.replace("$gui", "0")
                        knob.setExpression(new_knob_expr, idx)
                        knob.clearAnimated(idx)

        if has_gui_expression:
            print(f'Removed $gui expressions from {sel.name()}')
        else:
            # Handle ScanlineRender node specifically
            if sel.Class() == 'ScanlineRender':
                smpl = int(sel['samples'].value())
                sel['samples'].setExpression('$gui ? 2 : %s' % smpl)
                print(f'Added $gui expression to samples knob of {sel.name()}')
            # General handling for 'disable' knob
            elif sel.knob('disable'):
                sel['disable'].setExpression('$gui')
                print(f'Added $gui expression to disable knob of {sel.name()}')
            else:
                print('skipped $gui handling')
