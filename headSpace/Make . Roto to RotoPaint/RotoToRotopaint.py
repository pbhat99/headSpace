########## ROTO to ROTOPAINT v1.1 ##########
## convert your roto node into rotopaint ###
########### by ANDREA GEREMIA ##############
#--------------------------------------------------
#--------------------------------------------------

import nuke

try:
  from PySide.QtGui import QApplication
except:
  from PySide2.QtWidgets import QApplication

#-------------------------------------------------
#deselect nodes
def deselectAll():
    for n in nuke.selectedNodes():
        n['selected'].setValue(False)

#------------------------------------------------

def copy_paste():
    #set clipboard
    nuke.nodeCopy("%clipboard%")
    
    deselectAll()

    #read clipboard
    t = QApplication.clipboard().text()

    #replace only 2 strings Roto
    t = t.replace("Roto", "RotoPaint", 2)
    #print t
    
    #Qt way to store something in the clipboard
    QApplication.clipboard().setText(t)
    
    nuke.nodePaste('%clipboard%')

#-------------------------------------------------

def RotoToRotopaint():
	nodes = nuke.selectedNodes()    # GET SELECTED NODES
	amount = len( nodes )    # GET NUMBER OF SELECTED NODES
	
	
	if amount == 1:
	    node = nuke.selectedNode()
	    if (node.Class() == "Roto"):
	        copy_paste()
	    else:
	        nuke.message("Select a Roto node")
	else:
	    nuke.message("Select only one Roto node")