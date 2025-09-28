# headSpace tools for nuke

This includes various python tools & nuke Grizmos to work as a efficient compositor. All tools are tested on nukex 12 & nukex14 on windows 11 OS environment. Some of the tools & Grizmos are tweaked for my needs & ease of use from my perspective. I will try to keep it updated when the new version of tool is released. Most of the tools are sourced from [Nukepedia](https://www.nukepedia.com/) & I don't own them.

## Installation:

1.  Copy the entire directory to your nuke plugin path (Suggested .nuke folder in your user folder) [More info...](https://support.foundry.com/hc/en-us/articles/207271649-Q100048-Nuke-Directory-Locations)
    ```python
    Linux : /home/<username>/.nuke
    Mac : /Users/<username>/.nuke
    Windows : C:\Users\<username>\.nuke
    ```
2.  Add the below lines to init.py file (if none create one)
    ```python
    nuke.pluginAddPath('./headSpace')
    ```

## Compatibility:

*   Actively testing on **NukeX 12.2v11** and It will not cause any effect on launching letest versions of NukeX.
*   Works on Windows (11) & linux (ubuntu & centOS). Not tested on Mac yet (but it should work)

## Customization:

*   You can change this main folder name (headSpace) whatever you want (usually your name :P ), It will show same name in nuke menubar.
*   for submenus you need to add 'space-dot-space' in folder name
*   If something is not working, incase of error or your company already has that tool, Just delete that folder located inside main folder. Its totally independent.
*   Gizmos(or toolsets with .nk extensions) are Auto populated according to folder structure along with icon having same name.
*   Works best along with [Nuke servival toolkit](https://github.com/CreativeLyons/NukeSurvivalToolkit_publicRelease) (not included in this)

## List of python tools In this repo:

### Animation

*   **[Animation Maker](https://www.nukepedia.com/python/ui/animation-maker/)**: A python/pyside extension to Nuke giving you prebuilt ease and wave expressions on any animatable knob.
*   **[Reduce keyframes](https://richardfrazer.com/tools-tutorials/keyframe-reduction-script-for-nuke/)**: Reduces the number of keyframes in an animation curve.
*   **[LabelThisKnob](https://github.com/pbhat99/headSpace)**: Adds a button to the animation menu that allows you to quickly add knob value to the label.

### Axis

*   **[animated snap3D](http://www.nukepedia.com/python/3d/animatedsnap3d)**: This submodule contains the functions needed to execute an animated snap.

### DAG

*   **[Align Read Nodes](https://github.com/pbhat99/headSpace)**: Aligns selected read nodes in the node graph editor of the foundry's nuke.
*   **[Align Dots](https://www.nukepedia.com/python/nodegraph/aligndots)**: Puts the selected dot in a corner with its input and output node.
*   **[transformNodesTools](http://www.nukepedia.com/python/nodegraph/transformnodestools)**: A collection of simple node UI transform tools. Great for very large scripts. Lets you easily move/rotate/scale/mirror nodes with keyboard shortcuts.
*   **[W_Scaletree](https://www.nukepedia.com/python/nodegraph/w_scaletree)**: Scale the currently selected nodes.
*   **[W_Align](https://www.nukepedia.com/python/nodegraph/w_smartalign)**: if multiple nodes are selected, all the nodes will align to the node that's the furthest away in the specified direction.

### Viewer

*   **[QuickCreate](https://www.nukepedia.com/python/ui/quickcreate-for-nuke)**: Create nodes on selection from the viewer.
*   **[createShuffle](https://www.nukepedia.com/python/nodegraph/shufflefromviewer)**: Create a shuffle node from the viewer.

### Utilities

*   **[autoCrop](https://www.nukepedia.com/gizmos/transform/autocrop)**: Automatically crops the image based on the alpha channel.
*   **[Comma](https://www.nukepedia.com/gizmos/other/comma)**: A simple gizmo to add a comma to the label of a node.
*   **[Cycle Operations](https://www.nukepedia.com/python/nodegraph/cycleoperations)**: The most-used knob of the selected node will cycle through its options, forwards or backwards.
*   **[deleteViewers](https://github.com/pbhat99/headSpace)**: Deletes all viewers inside groups.
*   **[GrayAutoBackdrop](https://www.nukepedia.com/python/nodegraph/grayautobackdrop)**: Automatically puts a backdrop behind the selected nodes.
*   **[GUI Tool](https://github.com/pbhat99/headSpace)**: This handle GUI expression. if scanlineRender is selected sets the expression for sample knob. for all other nodes it sets $gui expression for disable knob if exists.
*   **[Multi Knob Edit](http://www.nukepedia.com/python/nodegraph/multiknobedit)**: Edit multiple knobs at once.
*   **[myMerge](https://github.com/pbhat99/headSpace)**: A custom merge node that intelligently chooses the merge operation based on the input nodes.
*   **[reLabeler](https://www.nukepedia.com/python/nodegraph/ku_labler)**: Mini Dialog to re-label nodes on the fly.

### Make

*   **[CameraBake](https://github.com/pbhat99/headSpace)**: Bakes a camera animation to a new camera.
*   **[CardInFrustum](https://github.com/pbhat99/headSpace)**: Make a card that is oriented towards the selected camera node, and fit it in its frustum.
*   **[cardsFromCamPath](https://github.com/pbhat99/headSpace)**: Create cards from a camera path.
*   **[clone Via Expressions_fxT](https://www.fxtor.net/)**: This script makes it safe to use clones again by swapping it out with expressions.
*   **[combine_retimes](https://www.nukepedia.com/python/time/combine-retimes)**: A python script that can combines a stack of multiple retiming nodes into a merged output.
*   **[Gizmo to Group](https://github.com/pbhat99/headSpace)**: Converts a gizmo to a group.
*   **[Nuke vector Matrix](https://erwanleroy.com/nuke-vector-matrix-toolset-beta-release/)**: Set of utility functions to perform matrix operations in Nuke.
*   **[Roto to rotopaint](https://www.nukepedia.com/python/nodegraph/roto-to-rotopaint)**: convert your roto node into rotopaint.
*   **[Tracker to Transform](https://github.com/pbhat99/headSpace)**: Replaces Trackers used in script with baked Transforms.
*   **[new_ref_frame](https://www.nukepedia.com/python/3d/new-ref-frame)**: This tool will help you to: A) Set a new reference frame for any Transform or CornerPin2D node. B) Generate data for MatchMove or Stabilize.

### Other

*   **[Channel Hotbox](https://www.nukepedia.com/python/ui/channel-hotbox)**: This module provides an Interface class to toggle and shuffle layer.
*   **[KnobScripter](https://github.com/adrianpueyo/KnobScripter/tree/release-v3.0.0)**: Complete python script editor for Nuke.
*   **[nukeSwitch](https://www.nukepedia.com/python/misc/nukeswitch)**: Switch between Nuke and NukeX.
*   **[Recent Files browser](https://www.nukepedia.com/python/ui/recent-files-browser)**: A recent files browser for Nuke.
*   **[SpeedyScript Trimmed](https://www.nukepedia.com/python/nodegraph/speedyscript)**: A trimmed down version of SpeedyScript.
*   **[TabTabTab](http://www.nukepedia.com/python/ui/tabtabtab)**: Alternative "tab node creator thingy" for The Foundry's Nuke.
*   **[W_hotbox](https://www.nukepedia.com/python/ui/w_hotbox)**: A hotbox for Nuke.
*   **[WrapItUp](https://maxvanleeuwen.com/project/collect-nuke-scripts-wrapitup/)**: Collect all media, gizmos and files associated with a nuke script, and copy it all to a separate folder - along with a relinked duplicate of the nuke script.
*   **[_sandWitcher](https://github.com/pbhat99/headSpace)**: A tool for creating toolsets.
*   **[autoLabels](https://github.com/pbhat99/headSpace)**: Automatically adds labels to nodes.
*   **[Drag and Drop](https://github.com/pbhat99/headSpace)**: Enhanced drag and drop functionality within Nuke.
*   **[KnobDefaults](https://github.com/pbhat99/headSpace)**: Personal default node settings.

### GRiZMOS:

#### Filter

*   **[Disturb](https://github.com/pbhat99/headSpace)**: Distorts the input image with a noise pattern.
*   **[FFfiller_v01](https://github.com/pbhat99/headSpace)**: A tool to fill holes in the alpha channel.
*   **[FireflyKiller](https://github.com/pbhat99/headSpace)**: Removes fireflies from the image.
*   **[LensSim](https://github.com/pbhat99/headSpace)**: A quick tool to add some level of 'lens simulation' to any image, preferably CG imagery.

#### Keyer

*   **[ScreenXchange_pb](https://www.nukepedia.com/gizmos/keyer/screenxchange)**: This tool is NOT a Keyer, because it doesn't output a Matte, instead it replaces a Green or Bluescreen with Background using a different math than usual Keying.
*   **[bm_EdgeMatte](https://github.com/BenMcEwan/nuke_public)**: Simple gizmo to get a clean, controllable outline (like Edge Detect) from any matte.
*   **[Erode (round)](https://github.com/pbhat99/headSpace)**: Erodes the input image with a round filter.
*   **[Erode_Fine](https://github.com/SpinVFX/spin_nuke_gizmos/)**: Erode an image with fine controls, as opposed to Nuke's default erode node.
*   **[KeyChew](https://github.com/pbhat99/headSpace)**: A tool to chew the matte.
*   **[Organic_edges](https://github.com/pbhat99/headSpace)**: Creates organic looking edges for your mattes.
*   **[Perimeter_v1.0](https://www.nukepedia.com/gizmos/keyer/perimeter)**: Perimeter is an advanced edge matte generation tool.

#### Other

*   **[AitorEcheveste](https://github.com/pbhat99/headSpace)**: A collection of gizmos from Aitor Echeveste.
    *   **aeAnamorphic**: A tool to simulate anamorphic lens distortion.
    *   **aeBrokenEdges**: A tool to break the edges of a matte.
    *   **aeBrokenShapes**: A tool to break shapes.
    *   **aeDirtCG**: A tool to add dirt to CG elements.
    *   **aeFiller**: A tool to fill holes in the alpha channel.
    *   **aeMotionBlur**: A tool to add motion blur to an image.
    *   **aePrefMaker**: A tool to create a prefix for your read nodes.
    *   **aeRefracTHOR**: A tool to create refractions.
    *   **aeRelight2D**: A tool to relight a 2D image.
    *   **aeTransform**: A tool to transform an image.
    *   **aeUVChart**: A tool to generate a UV chart.
    *   **iSTMap**: A tool to apply a STMap to an image.
    *   **iSTMap11**: A tool to apply a STMap to an image.
*   **[MangoSuite](https://github.com/pbhat99/headSpace)**: A collection of gizmos from Johannes Kretschmer.
    *   **ms_alphaeliminate**: This node will help to get rid of the little artifacts from the film plate noise that often stays after keying.
    *   **ms_alphafromrange**: This node lets you select every color that is above or below a certain value.
    *   **ms_antialias**: A tool to antialias an image.
    *   **ms_arrangeflares**: A tool to arrange flares.
    *   **ms_blendtransforms**: This node can blend between two different transformations.
    *   **ms_blendtransformslegacy**: This node can blend between two different transformations.
    *   **ms_brightness**: This node lets you affect just the brightness without changing the saturation like a normal grade would do.
    *   **ms_brightnesscontrast**: This node lets you affect the brightness and contrast of an image without changing the saturation.
    *   **ms_calculator**: A calculator for various Nuke specific calculations.

## Credits:

*   All goes to respected owners.
*   I will be happy if you thank me.

## Disclaimer:

*   all the tools here are publically availbale on the internet.
*   Some tools are modified to better fit & usability
*   Use at your own risk. I didn't responsible for damage.
