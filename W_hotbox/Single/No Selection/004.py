#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: gCheck
#
#----------------------------------------------------------------------------------------------------------

def gCheck():
 if not nuke.selectedNodes() == None:
  for i in nuke.allNodes('Viewer'):
   i.setSelected(True)

 nuke.display('gList()', nuke.selectedNode(), 'Gizmos Found in this Script:')

def gList():
 gzm = ''
 for i in nuke.allNodes():
  kn = i.knobs()
  if 'gizmo_file' in kn :
   gzm = gzm + '\n\n' + i.name()
 return gzm

gCheck()