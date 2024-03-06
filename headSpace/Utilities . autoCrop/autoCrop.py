# @Author: Kire Timov
# @Date:   Saturday, May 26th 2018, 6:45:53 am
# @Email:  vfxvision@gmail.com
# @Project: Auto Crop v1.1
# @Last modified by:   Kire Timov
# @Last modified time: Sunday, June 10th 2018, 2:24:13 am
# @Copyright: # @ Copyright (c) 2017, Kire Timov
# @ All rights reserved.
# @
# @ Redistribution and use in source and binary forms, with or without
# @ modification, are permitted provided that the following conditions are met:
# @     * Redistributions of source code must retain the above copyright
# @       notice, this list of conditions and the following disclaimer.
# @     * Redistributions in binary form must reproduce the above copyright
# @       notice, this list of conditions and the following disclaimer in the
# @       documentation and/or other materials provided with the distribution.
# @     * Redistribution of this software in source or binary forms shall be free
# @       of all charges or fees to the recipient of this software.
# @
# @ THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER "AS IS" AND
# @ ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# @ WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# @ DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# @ DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# @ (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# @ LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# @ ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# @ (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# @ SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import nuke
import nukescripts

globalFirstFrame = str(int(nuke.root().knob('first_frame').value()))
globalLastFrame = str(int(nuke.root().knob('last_frame').value()))


def selectionCheck():
    selection = nuke.selectedNodes()
    for i in selection:
        if range(len(selection)) == 0:
            return False
        else:
            return selection


def allDependentNodesAndInputs(node, deepNumber):

    dependent = node.dependent()
    dependentInputs = []
    for d in dependent:
        x = 0
        while x <= deepNumber:
            if d.input(x) == node:
                dependentInputs.append([d, x])
            x = x + 1
    return dependentInputs


class autoCropPanel(nukescripts.PythonPanel):

    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'Auto Crop', 'com.ohufx.autoCrop')

        self.about = nuke.Text_Knob(
            'about', '<b><font size="3" color="cyan">&nbsp;&nbsp;Auto Crop</font></b>',
            ' ' * 28 + 'Kire Timov  |  vfxvision@gmail.com')
        self.frange = nuke.Enumeration_Knob('frange', 'range', ['input', 'global', 'custom'])
        self.frameRange = nuke.String_Knob('frameRange', '')
        self.frameRange.clearFlag(nuke.STARTLINE)
        self.channels = nuke.Channel_Knob('channels', 'channels')
        self.overscan = nuke.Boolean_Knob('overscan', 'overscan', True)
        self.overscan.setFlag(nuke.STARTLINE)
        self.safety = nuke.Boolean_Knob('safety', 'add additional 30 safety pixels', True)

        self.addKnob(self.about)
        self.addKnob(self.frange)
        self.addKnob(self.frameRange)
        self.frameRange.setValue('the input range for each selected input')
        self.frameRange.setFlag(0x00000080)  # disable the frange field
        self.addKnob(self.channels)
        self.channels.enableChannel(3, True)  # check the alpha channel by default
        self.addKnob(self.overscan)
        self.addKnob(self.safety)

    def knobChanged(self, knob):
        # Determine the frame range
        if knob == self.frange:
            if self.frange.value() == 'input':
                self.frameRange.setFlag(0x00000080)
                self.frameRange.setValue('the respective range for each selected input')
            elif self.frange.value() == 'global':
                self.frameRange.setFlag(0x00000080)
                self.frameRange.setValue(globalFirstFrame + '-' + globalLastFrame)
            elif self.frange.value() == 'custom':
                self.frameRange.clearFlag(0x00000080)
                self.frameRange.setValue(globalFirstFrame + '-' + globalLastFrame)

    def autoCropMainCode(self):
        def praseCustomRange():
            if self.frameRange.value().isdigit():
                return [self.frameRange.value(), self.frameRange.value()]
            else:
                cleanString = ''.join(c for c in self.frameRange.value() if c.isdigit() or c == '-')
                noSpaces = cleanString.replace(' ', '')
                fRange = noSpaces.split('-')
                return fRange

        selection = selectionCheck()

        for i in selection:
            i['selected'].setValue(False)

        for i in selection:
            adni = allDependentNodesAndInputs(i, 50)
            i['selected'].setValue(True)
            curveTool = nuke.nodes.CurveTool()
            curveTool.setInput(0, i)
            if self.overscan.value() is True:
                curveTool['ROI'].setExpression('input.bbox.x', 0)
                curveTool['ROI'].setExpression('input.bbox.y', 1)
                curveTool['ROI'].setExpression('input.bbox.r', 2)
                curveTool['ROI'].setExpression('input.bbox.t', 3)
            else:
                curveTool['resetROI'].execute()

            curveTool['channels'].fromScript(self.channels.toScript())
            curveTool['operation'].setValue('Auto Crop')

            if self.frange.value() == 'input':
                nuke.execute(curveTool, int(i.firstFrame()), int(i.lastFrame()))
            if self.frange.value() == 'global':
                nuke.execute(curveTool, int(globalFirstFrame), int(globalLastFrame))
            if self.frange.value() == 'custom':
                tmpRange = praseCustomRange()
                nuke.execute(curveTool, int(tmpRange[0]), int(tmpRange[1]))

            crop = nuke.nodes.Crop()
            crop.setInput(0, curveTool)
            crop['box'].copyAnimations(curveTool['autocropdata'].animations())
            if self.safety.value():
                crop['box'].setExpression('curve - 15', 0)
                crop['box'].setExpression('curve - 15', 1)
                crop['box'].setExpression('curve + 15', 2)
                crop['box'].setExpression('curve + 15', 3)
            crop['label'].setValue('Auto Crop')
            crop['selected'].setValue(False)
            nuke.delete(curveTool)

            for d in adni:
                d[0].setInput(d[1], crop)


def autoCrop():
    initClass = autoCropPanel()

    if selectionCheck() is not None:
        if initClass.showModalDialog():
            initClass.autoCropMainCode()
    else:
        nuke.message('Please select one or more inputs that you want to crop')
