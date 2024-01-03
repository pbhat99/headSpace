import sys
import nuke
import os

#*****************************************************************
#*****************************************************************
#******************ADD THIS TO YOUR FILE INIT.PY******************
#SpeedyScript_path = "/Users/yourPath/.nuke/SpeedyScript"
#nuke.pluginAddPath(SpeedyScript_path)
#*****************************************************************
#*****************************************************************

#IMPORT SPEEDY SCRIPT
import SpeedyScript
paneMenu = nuke.menu('Pane')
paneMenu.addCommand('SpeedyScript', SpeedyScript.addSSPanel)
nukescripts.registerPanel('com.ohufx.SpeedyScript', SpeedyScript.addSSPanel)




#*****************************************************************
#*****************************************************************
#CREATE BUTTON IN THE READ NODES when READ NODE is CREATED
def createReadNodesFunction():
    import ReadNodes_ImportScript  
    
    n = nuke.thisNode()

    
    metad = 'exr/nuke/script/script' #'exr/nuke/script/script'
    
    #CREATE KNOBS
    tabKnob = nuke.Tab_Knob('Import Script')
    importKnob = nuke.PyScript_Knob("Import Script into Group","<font color='red'>Import Script into Group","import ReadNodes_ImportScript \nReadNodes_ImportScript.getScriptPath()")
    openKnob= nuke.PyScript_Knob("Open Script","<font color='deepskyblue'>Open Script","import ReadNodes_ImportScript \nReadNodes_ImportScript.OpenScript()")
    dividerKnob = nuke.Text_Knob("divider","")
    
    n.addKnob(tabKnob)
    n.addKnob(importKnob)
    n.addKnob(openKnob)
    
#*****************************************************************
#*****************************************************************  
#DISABLE/DELETE THE LINE BELOW IF YOU DON'T WANT THE NEW TAB IN EVERY READ NODE
#nuke.addOnUserCreate(lambda: createReadNodesFunction(), nodeClass="Read")    



mainMenu = menuMaker()
nuke.menu('Nuke').addCommand(mainMenu + 'Speedy Script/import script as Group', "import SpeedyScriptLight ; SpeedyScriptLight.importScriptFunction(nuke.getFilename('Please Select'))", icon='SpeedyScript.png')
nuke.menu('Nuke').addCommand(mainMenu + 'Speedy Script/Export Group as Grizmo', "import SpeedyScriptLight ; SpeedyScriptLight.exportScriptFunction()", icon='SpeedyScript.png')
nuke.menu('Nuke').addCommand(mainMenu + 'Speedy Script/Find Imported Group', "import SpeedyScriptLight ; SpeedyScriptLight.findGroupFunction()", icon='SpeedyScript.png')