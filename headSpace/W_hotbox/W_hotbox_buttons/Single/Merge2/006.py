#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: conjoint/disjoint/over
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('operation').value() == 'over':
        i.knob('operation').setValue('conjoint-over')
    elif i.knob('operation').value() == 'conjoint-over':
        i.knob('operation').setValue('disjoint-over')
    elif i.knob('operation').value() == 'disjoint-over':
        i.knob('operation').setValue('over')
    else:
        i.knob('operation').setValue('over')
        
        