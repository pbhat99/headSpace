#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: # Set ref
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    
    #reset expression
    TKnob = i.knob('translate')
    TKnob.setExpression("" ,0)
    TKnob.setExpression("" ,1)
    
    #minus current Value
    TX = "curve-" + str(i.knob("translate").value(0))
    TY = "curve-" + str(i.knob("translate").value(1))
    
    #set expression
    TKnob.setExpression(TX ,0)
    TKnob.setExpression(TY ,1)
    
#    i.knob('rotate').setExpression((tr="curve-" + 'str(i.knob("translate").value(1))') ,0)