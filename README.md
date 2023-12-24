# headSpace tools for nuke
   This includes various pythhon tools & nuke Grizmos to work as a efficient compositor.
All tools are tested on nukex 12 & nukex14 on windows 11 OS environment.
Some of the tools & Grizmos are tweaked for my needs & ease of use from my perspective.
I will try to keep it updated when the new version of tool is released.
Most of the tools are sourced from [Nukepedia](https://www.nukepedia.com/) & I don't own them.

## Installation:
 1. Copy the entire directory to your nuke plugin path (Suggested .nuke folder in your user folder) [More info...](https://support.foundry.com/hc/en-us/articles/207271649-Q100048-Nuke-Directory-Locations)
   ```python
   Linux : /home/<username>/.nuke
   Mac : /Users/<username>/.nuke
   Windows : C:\Users\<username>\.nuke
   ```

 2. Add the below lines to init.py file (if none create one)
   ```python
   nuke.pluginAddPath('./headSpace')
   ```
 

## Customization:
- You can change this main folder name whatever you want, It will show same name in nuke menubar.
- for submenus youu need to add '<space><dot><space>' in folder name
- If something is not working or incase of error Just delete that folder inside main folder. Its totally independent.
- Gizmos are Auto populated according to folder structure along with icon having same name.
- 

## List of tools In this repo:

- **axis Menu:**
  - [animated snap3D](http://www.nukepedia.com/python/3d/animatedsnap3d)

- **animation Menu:**
  - [Animation Maker](https://www.nukepedia.com/python/ui/animation-maker/) 
  - [Reduce keyframes](https://richardfrazer.com/tools-tutorials/keyframe-reduction-script-for-nuke/) 

- **Viewer Menu:**
  - [QuickCreate](https://www.nukepedia.com/python/ui/quickcreate-for-nuke) 
  - [createShuffle](https://www.nukepedia.com/python/nodegraph/shufflefromviewer) 

- **Nuke Menubar:**
  - **Help->**
    - About
    - Github
  - **DAG->**
   - Align Read Nodes
   - [Align Dots](https://www.nukepedia.com/python/nodegraph/aligndots) 
   - [Mirror Nodes](https://www.nukepedia.com/python/nodegraph/mirrornodes) 
   - [W_Scaletree](https://www.nukepedia.com/python/nodegraph/w_scaletree) 
   - [W_Align](https://www.nukepedia.com/python/nodegraph/w_smartalign)

  - **Utilities->**
    - [Comma](https://www.nukepedia.com/gizmos/other/comma) 
    - [Cycle Operations](https://www.nukepedia.com/python/nodegraph/cycleoperations) 
    - [GrayAutoBackdrop](https://www.nukepedia.com/python/nodegraph/grayautobackdrop) 
    - GUI Tool
    - reLabeler

  - **Make->**
    - Camera Bake
    - Card in Frustrum
    - Cards along camera path
    - Combine retimes
    - Combine transforms
    - Gizmos to Group
    - Nuke vector Matrix
    - Roto to rotopaint
    - Tracker to Transform
    - Clone via Expressions

  - Channel Hotbox
  - [Tab Tab Tab](http://www.nukepedia.com/python/ui/tabtabtab) 
  - [Welcome Screen](http://www.nukepedia.com/python/ui/welcomescreen) 
  - [WrapItUp](https://maxvanleeuwen.com/project/collect-nuke-scripts-wrapitup/) 
  - [W_hotbox](https://www.nukepedia.com/python/ui/w_hotbox)   (with default & custom buttons)
  - [KnobScripter](https://github.com/adrianpueyo/KnobScripter/tree/release-v3.0.0) 
  - [Stamps](https://adrianpueyo.com/stamps/) 


- **GRiZMOS:**
  - GizmoPathManager from SpinVFX
  - AitorEcheveste Tools
  - nuke-vector-matrix
  - pixelfudger3
  - etc

- **No UI:**
  - Drag & drop
    - DropDataHandler
    - gizmoDropper
  - W_MoveMenu
  - Quick Shortcut editor
  - KnobDefaults



