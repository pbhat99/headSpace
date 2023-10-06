# Replaces Trackers used in script with baked Transforms.
# Can take a while to process.
# Sven Ahlström, sven.ahlstrom@gmail.com

import nuke


def trackerToTransform():
    for i in nuke.selectedNodes('Tracker4'):
        if i.dependencies() and i.dependent():
            refFrame = "Ref " + str(int(i['reference_frame'].value()))
            typ = i['transform'].value()
            if typ == 'stabilize' or typ == 'satbilize 1-pt':
                val = 6
            else:
                val = 7
            dot = nuke.createNode('Dot', inpanel=False)
            dependents = i.dependent()
            
            i['cornerPinOptions'].setValue(val)
            old = nuke.allNodes('Transform')
            i['createCornerPin'].execute()
            pin = [n for n in nuke.allNodes('Transform') if n not in old][0]
            pinpos = [pin.xpos(), pin.ypos()]
    
            pin['label'].setValue(refFrame)
            pin.setInput(0, i.dependencies()[0])
            pin.setXYpos(i.xpos(), i.ypos())
            i.setXYpos(pinpos[0], pinpos[1])
            dot.setInput(0, pin)
            i.setInput(0, None)
            nuke.delete(dot)