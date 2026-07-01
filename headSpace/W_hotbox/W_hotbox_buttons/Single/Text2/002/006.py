#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Env Variable
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
        i.knob('message').setValue('[python os.environ.get("PROJECT")]')