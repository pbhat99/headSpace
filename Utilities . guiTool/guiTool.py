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
    try:
        sel = nuke.selectedNode()

        if sel.Class() == 'ScanlineRender':
            if sel['samples'].hasExpression():
                sel['samples'].clearAnimated()
                sel['label'].setValue('')
            else:
                smpl = int(sel['samples'].value())
                sel['samples'].setExpression('$gui ? %s : 16'%(smpl))
                sel['label'].setValue('<b>GUI Sample</b>')
        elif sel.knob('disable'):
            if sel['disable'].hasExpression():
                sel['disable'].clearAnimated()
                sel['disable'].setValue(0)
                sel['label'].setValue('')
            else:
                sel['disable'].setExpression('$gui') # for general use
                #sel['disable'].setExpression('[python {1-nuke.executing()}]') # if u need local render support
                sel['label'].setValue('<b>GUI disabled</b>')
        else:
            pass
    except:
        nuke.createNode("guiHandler")



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