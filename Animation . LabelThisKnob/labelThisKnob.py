#adds button to animation menu that allows you to quickly add knob value to label
#installation:
#put this file in ~/.nuke folder(or to any other nuke's plug-in path folder)
#paste this line to menu.py
#import labelThisKnob

#v1.0
#created by: Pushkarev Aleksandr
#e-mail: pushkarevalecsandr@gmail.com

import nuke

def addLabel(node,label):
    kn = node.knob('label')
    value = kn.value()
    if not value.count(label):
        if value:
            label = '\n'+label
        kn.setValue(value+label)
        node.setYpos(node.ypos()-6)

def labelThis():
    node = nuke.thisNode()
    kn = nuke.thisKnob()
    if kn.label():
        label = kn.label().title()+' : [value '+kn.name()+']'
    else:
        label = kn.name().title()+' : [value '+kn.name()+']'
    addLabel(node,label)