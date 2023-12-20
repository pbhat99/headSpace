def smMerge(nodeType):
    import nuke
    a = nuke.selectedNodes()
    al = []
    for node in a:
        al.append(node['xpos'].value())
        al.sort()
        al.reverse()


    amm =  len(al)
    new = [None]*amm
    p = 0
    while p< amm:  
        a = nuke.selectedNodes()
        for one in a:
            pos = one['xpos'].value()
            if pos == al[p]:
                new.insert(p,one)
        p+=1

    q=1
    connected = 0
    merges = []
    for node in new[:amm]:
        if q==1:
            followed = node

            a = nuke.allNodes()### trying to connect downstream
            for anode in a:
                if anode.dependencies() == new[:1]:
                    depNode = anode
                    connected = 1

            q+=1
        else:
            if nodeType== "MergeGeo":
                follower = nuke.nodes.MergeGeo()
                #merges.append(follower)
            if nodeType== "MergeMat":
                follower = nuke.nodes.MergeMat()
                #merges.append(follower)
            if nodeType== "DeepMerge":
                follower = nuke.nodes.DeepMerge()
                #merges.append(follower)
            if nodeType== "Merge2":
                follower = nuke.nodes.Merge2()
                #merges.append(follower)
            follower.setInput(0,followed)
            follower.setInput(1,node)
            followed = follower
            merges.append(follower)
    if connected == 1:
        depNode.setInput(0,follower)
    for node in nuke.allNodes():
        node.setSelected(False)
    for node in merges:
        node.setSelected(True)


def mergeThis():
    import nuke
    try:
        nName = nuke.selectedNode()['name'].value()
        #getting the class name and getting rid of a version
        nClass = nuke.selectedNode().Class()
        tail = 0
        for one in nClass:
            if one.isdigit():
                tail = tail+1
        if tail >0:
            nClass = nClass[:-tail]
        nKnobs = nuke.selectedNode().knobs()
        shaders = ["AmbientOcclusion","BasicMaterial","FillMat","MergeMat","BlendMat","Project3D","Diffuse","Emission","Phong","Specular","Displacement","UVTile","Wireframe","Transmission"]
        
        if 'shadow_override' in nKnobs \
            or 'Camera' in nClass \
            or 'render_mode' in nKnobs \
            or 'Light' in nClass \
            or 'DisplaceGeo' in nClass \
            or 'Axis' in nClass:
            if len(nuke.selectedNodes())==1:
                return nuke.createNode( "MergeGeo")
            else:
                smMerge("MergeGeo")

        elif nClass in shaders:
            if len(nuke.selectedNodes())==1:
                return nuke.createNode( "MergeMat")
            else:
                smMerge("MergeMat")
        elif 'Deep' in nClass \
            and "DeepHoldout" not in nName \
            and "DeepToImage" not in nName \
            or "DeepRecolorMatte" in nName:
            if len(nuke.selectedNodes())==1:
                return nuke.createNode( "DeepMerge")
            else:
                smMerge("DeepMerge")
        else:
            raise ValueError
    except:
         if len(nuke.selectedNodes())<=1:
            return nuke.createNode( "Merge2")

         else:
            smMerge("Merge2")