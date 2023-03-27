#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: DownStream
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	for d in i.dependent():
		d.setSelected(True)