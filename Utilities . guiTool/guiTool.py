#------------------------------------------------------------------------------

#  $GUI Toggle
# 

#------------------------------------------------------------------------------
def guiTool():
    if not nuke.selectedNodes():
        nuke.createNode("Blur")

    for node in nuke.selectedNodes():
        disable_knob = node['disable']

        if node.Class() == 'ScanlineRender':
            samples_knob = node['samples']

            current_expr = samples_knob.toScript()

            if samples_knob.toScript() == {'$gui ? 1 : 8'}:
                samples_knob.clearAnimated()
                samples_knob.setValue(0)
            else:
                samples_knob.setExpression('$gui ? 1 : 8')

        current_expr = disable_knob.toScript()

        if disable_knob.toScript() == {'$gui'}:
            disable_knob.clearAnimated()
            disable_knob.setValue(0)
        else:
            disable_knob.setExpression('$gui')




#------------------------------------------------------------------------------
#  $GUI Toggle
#------------------------------------------------------------------------------
def disableGUI():
    for dis in nuke.selectedNodes():
        if dis['disable'].hasExpression():
            dis['disable'].clearAnimated()
            dis['disable'].setValue(0)
        else:
            dis['disable'].setExpression('$gui') # for general use
            #dis['disable'].setExpression('[python {1-nuke.executing()}]') # if u need local render support
    return