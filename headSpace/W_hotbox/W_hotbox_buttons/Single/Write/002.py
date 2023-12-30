#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Farm It!
#
#----------------------------------------------------------------------------------------------------------

print ('submitting to farm...\n ----------------------- \n')

nuke.root()['proxy'].setValue(0)
print ('proxy turned off\n ----------------------- \n')

nuke.scriptSave("")
print ('script saved\n ----------------------- \n')

rng = nuke.root().knob('last_frame').value() -nuke.root().knob('first_frame').value()
rng = int((rng/5)+1)

import sickle_nuke
sickle_nuke.farm_panel(outputs_from_selection=True, chunks=rng,rendergroup=2)

#from mill_farmer_2 import MillFarm2
#MillFarm2.farm_panel(outputs_from_selection=True, chunks=rng,)
