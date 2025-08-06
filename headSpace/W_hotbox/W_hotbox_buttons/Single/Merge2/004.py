#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: InvOp
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('operation').value() == 'over':
        i.knob('operation').setValue('under')
    elif i.knob('operation').value() == 'under':
        i.knob('operation').setValue('over')
    elif i.knob('operation').value() == 'mask':
        i.knob('operation').setValue('stencil')
    elif i.knob('operation').value() == 'stencil':
        i.knob('operation').setValue('mask')
    elif i.knob('operation').value() == 'from':
        i.knob('operation').setValue('minus')
    elif i.knob('operation').value() == 'minus':
        i.knob('operation').setValue('from')
    elif i.knob('operation').value() == 'max':
        i.knob('operation').setValue('min')
    elif i.knob('operation').value() == 'min':
        i.knob('operation').setValue('max')
    elif i.knob('operation').value() == 'in':
        i.knob('operation').setValue('out')
    elif i.knob('operation').value() == 'out':
        i.knob('operation').setValue('in')
    else:
        pass