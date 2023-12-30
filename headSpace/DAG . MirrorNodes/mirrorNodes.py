#------------------------------------------------------------------------------
# Mirror nodes by Frank Rueter
#------------------------------------------------------------------------------

import nuke
import nukescripts
import time
import threading



try:
    range = xrange
except:
    pass

class MirrorNodes( threading.Thread ):
    def __init__(self, nodes, direction='x', axis='average'):
        threading.Thread.__init__( self )
        if len( nodes ) < 2:
            raise ValueError("At least two nodes have to be selected")
        if direction.lower() not in ('x', 'y'):
            raise ValueError("direction argument must be x or y")
        
        self.axis = axis
        self.posDict = {}
        self.nodes= nodes
        self.direction = direction
        self.__mirrorPos()
        
    #----------------------------------
    def __mirrorPos(self):
        '''Get the mirrored position for each node'''
        if self.direction == 'x':
            if self.axis == 'last':
                n = nuke.selectedNodes()[0]
                axis = float(n.xpos() + n.screenWidth() / 2)
            elif self.axis == 'first':
                n = nuke.selectedNodes()[-1]
                axis = float(n.xpos() + n.screenWidth() / 2)
            else:
                # use average
                positions = [n.xpos() + n.screenWidth() / 2 for n in self.nodes]
                axis = float(sum(positions)) / len(positions)
        else:
            if self.axis == 'last':
                n = nuke.selectedNodes()[0]
                axis = float(n.ypos() + n.screenHeight() / 2)
            elif self.axis == 'first':
                n = nuke.selectedNodes()[-1]
                axis = float(n.ypos() + n.screenHeight() / 2)
            else:
                # use average
                positions = [n.ypos() + n.screenHeight() / 2 for n in self.nodes]
                axis = float(sum(positions)) / len(positions)            

        for n in self.nodes:
            if self.direction == 'x':
                centrePos = n.xpos() + n.screenWidth()/2
                oldPos = n.xpos()
                newPos = centrePos - 2*( centrePos - axis ) - n.screenWidth()/2.0
            else:
                centrePos = n.ypos() + n.screenHeight()/2
                oldPos = n.ypos()
                newPos = centrePos - 2*( centrePos - axis ) - n.screenHeight()/2.0
            self.posDict[ n ] = ( oldPos, round( newPos ) )

    #----------------------------------
    def run( self ):
        incs = 10
        for i in range( incs ):
            for n in self.nodes:
                oldPos = self.posDict[ n ][ 0 ]
                newPos = self.posDict[ n ][ 1 ]
                curPos = oldPos + ( newPos - oldPos ) / incs * (i+1)
                if self.direction == 'x':
                    nuke.executeInMainThreadWithResult( n.setXpos, int(curPos) )
                else:
                    nuke.executeInMainThreadWithResult( n.setYpos, int(curPos) )
            time.sleep(.01)