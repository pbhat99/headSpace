#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Create cards
#
#----------------------------------------------------------------------------------------------------------

import random

selCam = nuke.selectedNode()

if selCam.Class() == "Camera2":

     p = nuke.Panel("Create Cards from Camera Path")
     p.addSingleLineInput("Start Frame:", str(selCam['translate'].getKeyList()[0]))
     p.addSingleLineInput("End Frame:", str(selCam['translate'].getKeyList()[-1]))
     p.addSingleLineInput("Create Card at every nth Frame:", "25")

     p.addButton("Cancel")
     p.addButton("OK")
     result = p.show()

     if not result == 0:
          fromFrame = int(p.value("Start Frame:"))
          toFrame = int(p.value("End Frame:"))
          cardEveryNthFrame = int(p.value("Create Card at every nth Frame:"))


          noOpNode = nuke.nodes.NoOp()
          noOpNode.setName("CardControls")
          lookupSlider = nuke.Double_Knob("DistanceFadeLookup")
          noOpNode.addKnob(lookupSlider)
          alphaMulti = nuke.Double_Knob("alphaMulti")
          noOpNode.addKnob(alphaMulti)
          noOpNode['alphaMulti'].setValue(1)
          randomXpos = nuke.Double_Knob("randomXpos")
          noOpNode.addKnob(randomXpos)
          randomYpos = nuke.Double_Knob("randomYpos")
          noOpNode.addKnob(randomYpos)
          randomZpos = nuke.Double_Knob("randomZpos")
          noOpNode.addKnob(randomZpos)
          randomZrot = nuke.Double_Knob("randomZrot")
          noOpNode.addKnob(randomZrot)
          randomXscale = nuke.Double_Knob("randomXscale")
          noOpNode.addKnob(randomXscale)
          addXscale = nuke.Double_Knob("addXscale")
          noOpNode.addKnob(addXscale)
          randomYscale = nuke.Double_Knob("randomYscale")
          noOpNode.addKnob(randomYscale)
          addYscale = nuke.Double_Knob("addYscale")
          noOpNode.addKnob(addYscale)
          seed = nuke.Int_Knob("seed")
          noOpNode.addKnob(seed)
          noOpNode['DistanceFadeLookup'].setAnimated()
          noOpNode['DistanceFadeLookup'].setValueAt(0,0)
          noOpNode['DistanceFadeLookup'].setValueAt(1,1)
          noOpNode['DistanceFadeLookup'].setValueAt(1,4)
          noOpNode['DistanceFadeLookup'].setValueAt(0,7)

          for frameNumber in range(fromFrame,toFrame,cardEveryNthFrame):
               newCard = nuke.nodes.Card2()
               newCard.setName("CardAtFrame_"+str(frameNumber))
               
               newCard['translate'].setExpression(str(selCam['translate'].valueAt(frameNumber,0))+"+(((random("+str(random.randint(-2500,2500))+"+"+noOpNode.name()+".seed)-0.5))*"+noOpNode.name()+".randomXpos)",0)
               newCard['translate'].setExpression(str(selCam['translate'].valueAt(frameNumber,1))+"+(((random("+str(random.randint(-2500,2500))+"+"+noOpNode.name()+".seed)-0.5))*"+noOpNode.name()+".randomYpos)",1)
               newCard['translate'].setExpression(str(selCam['translate'].valueAt(frameNumber,2))+"+(((random("+str(random.randint(-2500,2500))+"+"+noOpNode.name()+".seed)-0.5))*"+noOpNode.name()+".randomZpos)",2)
               newCard['scaling'].setExpression("1+(((random("+str(random.randint(-1500,2500))+"+"+noOpNode.name()+".seed)-0.5))*"+noOpNode.name()+".randomXscale) + "+noOpNode.name()+".addXscale",0)
               newCard['scaling'].setExpression("1+(((random("+str(random.randint(-1500,2500))+"+"+noOpNode.name()+".seed)-0.5))*"+noOpNode.name()+".randomYscale) + "+noOpNode.name()+".addYscale",1)
               newCard['rotate'].setValue(selCam['rotate'].valueAt(frameNumber))
               newCard['rotate'].setExpression(str(selCam['rotate'].valueAt(frameNumber,2))+"+(((random("+str(random.randint(-360,360))+"+"+noOpNode.name()+".seed)-0.5))*"+noOpNode.name()+".randomZrot)",2)
               newCard['uniform_scale'].setExpression(selCam.name()+".uniform_scale")
               newTimeOffset = nuke.nodes.TimeOffset()
               newTimeOffset['time_offset'].setValue(random.randint(-500,500))
               newTimeOffset.setInput(0,noOpNode)

               newGrade = nuke.nodes.Grade()
               newGrade['channels'].setValue("alpha")
               newGrade['white_clamp'].setValue(1)
               newGrade['multiply'].setExpression(noOpNode.name()+".DistanceFadeLookup(sqrt(pow2(("+selCam.name()+".translate.x - "+newCard.name()+".translate.x)) + pow2(("+selCam.name()+".translate.y - "+newCard.name()+".translate.y))+pow2(("+selCam.name()+".translate.z - "+newCard.name()+".translate.z))))")
               
               newGrade.setInput(0,newTimeOffset)
               
               globalGradeMulti = nuke.nodes.Grade()
               globalGradeMulti['channels'].setValue("alpha")
               globalGradeMulti['multiply'].setExpression(noOpNode.name()+".alphaMulti")
               
               globalGradeMulti.setInput(0,newGrade)

               newPremult = nuke.nodes.Premult()

               newPremult.setInput(0,globalGradeMulti)
               
               newCard.setInput(0,newPremult)
          
else:
     nuke.message("Select a Camera to create Cards from") 