#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set ref
#
#----------------------------------------------------------------------------------------------------------

for n in nuke.selectedNodes():
    n['from1'].fromScript(n['to1'].toScript())
    n['from1'].clearAnimated()
    n['from2'].fromScript(n['to2'].toScript())
    n['from2'].clearAnimated()
    n['from3'].fromScript(n['to3'].toScript())
    n['from3'].clearAnimated()
    n['from4'].fromScript(n['to4'].toScript())
    n['from4'].clearAnimated()
    n.knob('label').setValue('ref : ' + str(nuke.frame()))