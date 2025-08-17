#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: <font size = 55> &#10566;
#
#----------------------------------------------------------------------------------------------------------

#prev
for n in nuke.selectedNodes():
    op = int(n['operation'].getValue())
    if op > 0:
        n['operation'].setValue(op-1)
    else:
        n['operation'].setValue(29)