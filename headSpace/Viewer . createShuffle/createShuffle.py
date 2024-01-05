import nuke

# took from Shuffle from viewer script by Conrad Olson

def createShuffle():
    #get the channels currently being viewed
    viewedChannel = nuke.activeViewer().node()['channels'].value()

    try:
        shuffle = nuke.createNode('Shuffle2')
        shuffle['in1'].setValue(viewedChannel)
        shuffle['label'].setValue('[value in1]')
    except:
        shuffle = nuke.createNode('Shuffle')
        shuffle['in'].setValue(viewedChannel)
        shuffle['label'].setValue('[value in]')



def createShuffleAndReset():
    #get the channels currently being viewed
    viewedChannel = nuke.activeViewer().node()['channels'].value()

    try:
        shuffle = nuke.createNode('Shuffle2')
        shuffle['in1'].setValue(viewedChannel)
        shuffle['label'].setValue('[value in1]')
    except:
        shuffle = nuke.createNode('Shuffle')
        shuffle['in'].setValue(viewedChannel)
        shuffle['label'].setValue('[value in]')
        
    nuke.activeViewer().node()['channels'].setValue('rgba')