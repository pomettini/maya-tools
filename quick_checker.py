import maya.cmds as cmds


selected_objects = ""


# TEST Reset the scene to the original state
def TestResetScene():
    cmds.select(all=True)
    cmds.delete()


# TEST Reset hypeshade to the original state
def TestResetHypershade():
    materials = cmds.ls(type='shadingDependNode')
    cmds.delete(materials)


def NewCheckerMaterial():
    # Creates a new lambert
    myMaterial = cmds.shadingNode('lambert', asShader=True)
    # Creates a shading node for the file
    myChecker = cmds.shadingNode('checker', asTexture=True)

    myPlaceTex = cmds.shadingNode('place2dTexture', asUtility=True)

    cmds.setAttr(myPlaceTex+'.repeatU', 10)
    cmds.setAttr(myPlaceTex+'.repeatV', 10)

    cmds.connectAttr(myPlaceTex+'.outUV', myChecker+'.uv')

    cmds.connectAttr(myPlaceTex+'.outUvFilterSize', myChecker+'.uvFilterSize')

    cmds.connectAttr(myChecker+'.outColor', myMaterial+'.color')

    return myMaterial


def ApplyMaterialToSelectedMesh(material):
    global selected_objects
    # Gets the selected objects and applies the new material
    cmds.select(selected_objects)
    cmds.hyperShade(assign=material)


def QuickChecker():
    global selected_objects
    selected_objects = cmds.ls(sl=True)
    myMaterial = NewCheckerMaterial()
    ApplyMaterialToSelectedMesh(myMaterial)


def FunctionalTest1():
    # Resets everything
    TestResetScene()
    TestResetHypershade()
    # Creates a sphere
    cmds.polySphere(n='Object001')
    cmds.select('Object001')
    # Runs the script
    QuickChecker()


def FunctionalTest2():
    # Resets everything
    TestResetScene()
    TestResetHypershade()
    # Creates two spheres
    cmds.polySphere(n='Object001')
    cmds.polySphere(n='Object002')
    # Moves the spheres
    cmds.move(0, 0, 0, 'Object001')
    cmds.move(2, 0, 0, 'Object002')
    # Selects the spheres
    cmds.select('Object001')
    cmds.select('Object002', add=True)
    # Runs the script
    QuickChecker()


# FunctionalTest1()
# FunctionalTest2()
QuickChecker()
