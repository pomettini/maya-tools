# coding=utf-8

'''
Puts plane references in the scene automatically
Based on top, side and front

TODO:
* Make a level for each reference
* Function and global variables needs prefixes!
'''

import maya.cmds as cmds
from pymel.all import Callback
import re


# Enumerator that contains all the Plane types
class PlaneType(object):
    TOP = 'top'
    BOTTOM = 'bottom'
    SIDE_L = 'side_l'
    SIDE_R = 'side_r'
    FRONT = 'front'
    BACK = 'back'


# All the stuff about the reference planes will be put here
planes = {}


# TEST Reset the scene to the original state
def TestResetScene():
    cmds.select(all=True)
    cmds.delete()


# TEST Reset hypeshade to the original state
def TestResetHypershade():
    materials = cmds.ls(type='shadingDependNode')
    cmds.delete(materials)


# TEST Removes all the layers
def TestResetLayers():
    layers = cmds.ls(type='displayLayer')
    cmds.delete(layers)


def LoadImagePath(planeType):
    imgFilter = 'All Image files (*.jpg *.gif *.png);;'
    imgPath = cmds.fileDialog2(fileFilter=imgFilter, dialogStyle=1, fileMode=1)

    # I put the plane image on dictionary/ui only if it's valid
    if imgPath is not None:
        SetImagePath(planeType, imgPath[0])
        RefreshUIImgPath(planeType, imgPath[0])
    else:
        cmds.confirmDialog(m='Please enter a valid image path')


def SetImagePath(planeType, imagePath):
    global planes
    # I put the image path on the planes dictionary
    planes[planeType] = imagePath


def RefreshUIImgPath(planeType, imagePath):
    cmds.textField(planeType+'_field', edit=True, tx=str(imagePath))


def EmptyImgPath(planeType):
    global planes
    # I remove the plane from the dictionary and empty the text field
    del planes[planeType]
    cmds.textField(planeType+'_field', edit=True, tx=str(''))


def RefreshAllUIImgPath():
    for plane in planes:
        RefreshUIImgPath(plane, planes[plane])


def RemoveAllPlaneReferences():
    # I remove all the planes, materials and the reference layer
    refElements = cmds.ls('ref_*')
    cmds.delete(refElements)
    cmds.delete('ReferenceLayer')


def CreatePlane(planeType):
    global planes

    planeSize = cmds.intSliderGrp('plane_size', q=True, v=True)
    planeDistance = cmds.intSliderGrp('plane_distance', q=True, v=True)

    halfSize = (planeSize / 2.0)

    # If the user puts -1 as the plane distance all the planes will be on the origin
    if planeDistance is -1:
        planeDistance = -halfSize

    if planeType == PlaneType.TOP:
        # Top
        plane = cmds.polyPlane(n='ref_top', w=planeSize, h=planeSize, sx=1, sy=1, ax=(0, 1, 0))
        cmds.setAttr(plane[0]+'.translate', 0, -planeDistance, 0)

    elif planeType == PlaneType.BOTTOM:
        # Bottom
        plane = cmds.polyPlane(n='ref_bottom', w=planeSize, h=planeSize, sx=1, sy=1, ax=(0, 1, 0))
        cmds.setAttr(plane[0]+'.translate', 0, (planeSize + planeDistance), 0)
        cmds.setAttr(plane[0]+'.rotate', 0, 0, 180)

    elif planeType == PlaneType.SIDE_L:
        # Left Side
        plane = cmds.polyPlane(n='ref_side_l', w=planeSize, h=planeSize, sx=1, sy=1, ax=(1, 0, 0))
        cmds.setAttr(plane[0]+'.translate', (halfSize + planeDistance), halfSize, 0)
        cmds.setAttr(plane[0]+'.rotate', 180, 0, 180)

    elif planeType == PlaneType.SIDE_R:
        # Rignt Side
        plane = cmds.polyPlane(n='ref_side_r', w=planeSize, h=planeSize, sx=1, sy=1, ax=(1, 0, 0))
        cmds.setAttr(plane[0]+'.translate', -(halfSize + planeDistance), halfSize, 0)
        cmds.setAttr(plane[0]+'.rotate', 0, 0, 0)

    elif planeType == PlaneType.FRONT:
        # Front
        plane = cmds.polyPlane(n='ref_front', w=planeSize, h=planeSize, sx=1, sy=1, ax=(0, 0, 1))
        cmds.setAttr(plane[0]+'.translate', 0, halfSize, -(halfSize + planeDistance))

    elif planeType == PlaneType.BACK:
        # Back
        plane = cmds.polyPlane(n='ref_back', w=planeSize, h=planeSize, sx=1, sy=1, ax=(0, 0, 1))
        cmds.setAttr(plane[0]+'.translate', 0, halfSize, (halfSize + planeDistance))
        cmds.setAttr(plane[0]+'.rotate', 0, 180, 0)

    return plane


def ApplyTexture(mesh, texturePath):
    material = CreateMaterialFromPath(texturePath)
    cmds.select(mesh[0])
    cmds.hyperShade(assign=material)
    cmds.rename(material, mesh[0]+'_mat')


def CreateMaterialFromPath(texturePath):
    # Creates a new lambert
    myMaterial = cmds.shadingNode('lambert', asShader=True)
    # Creates a shading node for the file
    myFile = cmds.shadingNode('file', asTexture=True)
    # Creates a shading group
    myShadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    # Sets the texture path
    cmds.setAttr(myFile+'.fileTextureName', texturePath, type='string')
    # Assigns the Texture File Name to the Shading Group Shader
    cmds.connectAttr(myMaterial+'.outColor', myShadingGroup+'.surfaceShader')
    # Assigns the Texture Color to the Material Color
    cmds.connectAttr(myFile+'.outColor', myMaterial+'.color')
    # Returns the material
    return myMaterial


def SearchReferencesInFolder():
    global planes

    refDir = cmds.fileDialog2(dialogStyle=1, fileMode=3)

    # I do stuff on the directory only if it's not empty
    if refDir is None:
        cmds.confirmDialog(m='Please enter a valid directory path')
        return

    directory = refDir[0]
    files = cmds.getFileList(folder=directory)

    for file in files:
        # If the path is empty I don't add the plane
        if file is None:
            continue

        if re.search(r'top', file):
            planes[PlaneType.TOP] = directory+'/'+file
        elif re.search(r'bottom', file):
            planes[PlaneType.BOTTOM] = directory+'/'+file
        elif re.search(r'left', file):
            planes[PlaneType.SIDE_L] = directory+'/'+file
        elif re.search(r'right', file):
            planes[PlaneType.SIDE_R] = directory+'/'+file
        elif re.search(r'front', file):
            planes[PlaneType.FRONT] = directory+'/'+file
        elif re.search(r'back', file):
            planes[PlaneType.BACK] = directory+'/'+file

    RefreshAllUIImgPath()


def CreateReferenceLayer():
    # I create the Ref layer once and set it as a reference layer
    if not cmds.objExists('ReferenceLayer'):
        cmds.createDisplayLayer(n='ReferenceLayer', empty=True)
        cmds.setAttr('ReferenceLayer.displayType', 2)


def AddMeshToReferenceLayer(meshName):
    cmds.editDisplayLayerMembers('ReferenceLayer', meshName)


def EnableBackfaceCulling(meshName):
    cmds.setAttr(meshName[0]+'.backfaceCulling', 3)


def GeneratePlanes():
    global planes

    CreateReferenceLayer()

    for planeType in planes:
        plane = CreatePlane(planeType)
        ApplyTexture(plane, planes[planeType])
        AddMeshToReferenceLayer(plane)
        EnableBackfaceCulling(plane)


def FunctionalTest():
    global planes

    TestResetHypershade()
    TestResetScene()
    TestResetLayers()

    planes = {
        'top': '/Users/Giorgio/Desktop/TestBlueprints/top.png',
        'bottom': '/Users/Giorgio/Desktop/TestBlueprints/ref_bottom.png',
        'side_l': '/Users/Giorgio/Desktop/TestBlueprints/left.png',
        'side_r': '/Users/Giorgio/Desktop/TestBlueprints/caneright.png',
        'front': '/Users/Giorgio/Desktop/TestBlueprints/front.png',
        'back': '/Users/Giorgio/Desktop/TestBlueprints/img-back.png'
    }

    GeneratePlanes()


def InitUI():
    win_name = 'quick_ref_setup'

    if cmds.window(win_name, q=True, ex=True):
        cmds.deleteUI(win_name)

    cmds.window(win_name, t='Quick References Setup')
    cmds.window(win_name, e=True, height=100, width=600, sizeable=False)
    cmds.columnLayout(adj=True)

    cmds.intSliderGrp('plane_size', f=True, l='Plane Size', minValue=1, maxValue=10, value=5)
    cmds.intSliderGrp('plane_distance', f=True, l='Plane Distance', minValue=-1, maxValue=10, value=-1)

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Top', c=Callback(LoadImagePath, PlaneType.TOP))
    cmds.textField('top_field', w=450)
    cmds.button(label=' X ', c=Callback(EmptyImgPath, PlaneType.TOP))
    cmds.setParent('..')

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Bottom', c=Callback(LoadImagePath, PlaneType.BOTTOM))
    cmds.textField('bottom_field', w=450)
    cmds.button(label=' X ', c=Callback(EmptyImgPath, PlaneType.BOTTOM))
    cmds.setParent('..')

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Left Side', c=Callback(LoadImagePath, PlaneType.SIDE_L))
    cmds.textField('side_l_field', w=450)
    cmds.button(label=' X ', c=Callback(EmptyImgPath, PlaneType.SIDE_L))
    cmds.setParent('..')

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Right Side', c=Callback(LoadImagePath, PlaneType.SIDE_R))
    cmds.textField('side_r_field', w=450)
    cmds.button(label=' X ', c=Callback(EmptyImgPath, PlaneType.SIDE_R))
    cmds.setParent('..')

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Front', c=Callback(LoadImagePath, PlaneType.FRONT))
    cmds.textField('front_field', w=450)
    cmds.button(label=' X ', c=Callback(EmptyImgPath, PlaneType.FRONT))
    cmds.setParent('..')

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Back', c=Callback(LoadImagePath, PlaneType.BACK))
    cmds.textField('back_field', w=450)
    cmds.button(label=' X ', c=Callback(EmptyImgPath, PlaneType.BACK))
    cmds.setParent('..')

    cmds.rowLayout(nc=3)
    cmds.button(label='Remove References', h=50, w=200, c=Callback(RemoveAllPlaneReferences))
    cmds.button(label='Load from folder', h=50, w=200, c=Callback(SearchReferencesInFolder))
    cmds.button(label='Generate', h=50, w=200, c=Callback(GeneratePlanes))
    cmds.setParent('..')
    cmds.showWindow(win_name)


InitUI()
# FunctionalTest()
