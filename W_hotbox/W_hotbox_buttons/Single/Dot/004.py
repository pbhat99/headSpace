#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Label
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('label').setValue('[value input.name]')
    i.knob('note_font_color').setValue('1')