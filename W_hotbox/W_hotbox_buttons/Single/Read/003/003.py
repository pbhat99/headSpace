#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Open Comp
#
#----------------------------------------------------------------------------------------------------------

try:
    node=nuke.selectedNode()
    if node.Class()!='Read':
        nuke.message('Selected Node is not a Read') 
        pass
    else:
        nFile=node['file'].getValue()
        ncompDir=nFile.split('/')[:7]
        ncompDir='/'.join(ncompDir)+'/'+'scripts/'
        allScripts=[]
        for file in os.listdir(ncompDir):
        
            if '.nk' in file and '~' not in file and 'autosave' not in file:
                allScripts.append(file)
        allScriptsDict={}
        for script in allScripts:
            scriptPath=ncompDir+script
            allScriptsDict[script]=scriptPath
        
        lallScripts=' '.join(sorted(allScripts))
        print lallScripts
        
        p = nuke.Panel('Choose Script')
        p.addEnumerationPulldown('Script Versions', lallScripts)
          
        ret = p.show()
        scriptOpen= p.value('Script Versions')
        
        
        scriptOpen=allScriptsDict[scriptOpen]
        nuke.scriptOpen(scriptOpen)

except ValueError:
    nuke.message('No Nodes Selected')
