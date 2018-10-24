# coding=utf-8

'''
Puts plane references in the scene automatically
Based on top, side and front
TODO:
* Make a level for each reference
'''

import maya.cmds as cmds
from pymel.all import Callback
import re


# Enumerator that contains all the Plane types
class QSR_PlaneType(object):
    TOP = 'top'
    BOTTOM = 'bottom'
    SIDE_L = 'side_l'
    SIDE_R = 'side_r'
    FRONT = 'front'
    BACK = 'back'


# All the stuff about the reference planes will be put here
qsr_planes = {}


# TEST Reset the scene to the original state
def QSR_TestResetScene():
    cmds.select(all=True)
    cmds.delete()


# TEST Reset hypeshade to the original state
def QSR_TestResetHypershade():
    materials = cmds.ls(type='shadingDependNode')
    cmds.delete(materials)


# TEST Removes all the layers
def QSR_TestResetLayers():
    layers = cmds.ls(type='displayLayer')
    cmds.delete(layers)


def QSR_LoadImagePath(planeType):
    imgFilter = 'All Image files (*.jpg *.gif *.png);;'
    imgPath = cmds.fileDialog2(fileFilter=imgFilter, dialogStyle=1, fileMode=1)

    # I put the plane image on dictionary/ui only if it's valid
    if imgPath is not None:
        SetImagePath(planeType, imgPath[0])
        RefreshUIImgPath(planeType, imgPath[0])
    else:
        cmds.confirmDialog(m='Please enter a valid image path')


def QSR_SetImagePath(planeType, imagePath):
    global qsr_planes
    # I put the image path on the planes dictionary
    qsr_planes[planeType] = imagePath


def QSR_RefreshUIImgPath(planeType, imagePath):
    cmds.textField(planeType+'_field', edit=True, tx=str(imagePath))


def QSR_EmptyImgPath(planeType):
    global qsr_planes
    # I remove the plane from the dictionary and empty the text field
    del qsr_planes[planeType]
    cmds.textField(planeType+'_field', edit=True, tx=str(''))


def QSR_RefreshAllUIImgPath():
    for plane in qsr_planes:
        RefreshUIImgPath(plane, qsr_planes[plane])


def QSR_RemoveAllPlaneReferences():
    # I remove all the planes, materials and the reference layer
    refElements = cmds.ls('ref_*')
    cmds.delete(refElements)
    cmds.delete('ReferenceLayer')


def QSR_CreatePlane(planeType):
    global qsr_planes

    planeSize = cmds.intSliderGrp('plane_size', q=True, v=True)
    planeDistance = cmds.intSliderGrp('plane_distance', q=True, v=True)

    halfSize = (planeSize / 2.0)

    # If the user puts -1 as the plane distance all the planes will be on the origin
    if planeDistance is -1:
        planeDistance = -halfSize

    if planeType == QSR_PlaneType.TOP:
        # Top
        plane = cmds.polyPlane(n='ref_top', w=planeSize, h=planeSize, sx=1, sy=1, ax=(0, 1, 0))
        cmds.setAttr(plane[0]+'.translate', 0, -planeDistance, 0)

    elif planeType == QSR_PlaneType.BOTTOM:
        # Bottom
        plane = cmds.polyPlane(n='ref_bottom', w=planeSize, h=planeSize, sx=1, sy=1, ax=(0, 1, 0))
        cmds.setAttr(plane[0]+'.translate', 0, (planeSize + planeDistance), 0)
        cmds.setAttr(plane[0]+'.rotate', 0, 0, 180)

    elif planeType == QSR_PlaneType.SIDE_L:
        # Left Side
        plane = cmds.polyPlane(n='ref_side_l', w=planeSize, h=planeSize, sx=1, sy=1, ax=(1, 0, 0))
        cmds.setAttr(plane[0]+'.translate', (halfSize + planeDistance), halfSize, 0)
        cmds.setAttr(plane[0]+'.rotate', 180, 0, 180)

    elif planeType == QSR_PlaneType.SIDE_R:
        # Rignt Side
        plane = cmds.polyPlane(n='ref_side_r', w=planeSize, h=planeSize, sx=1, sy=1, ax=(1, 0, 0))
        cmds.setAttr(plane[0]+'.translate', -(halfSize + planeDistance), halfSize, 0)
        cmds.setAttr(plane[0]+'.rotate', 0, 0, 0)

    elif planeType == QSR_PlaneType.FRONT:
        # Front
        plane = cmds.polyPlane(n='ref_front', w=planeSize, h=planeSize, sx=1, sy=1, ax=(0, 0, 1))
        cmds.setAttr(plane[0]+'.translate', 0, halfSize, -(halfSize + planeDistance))

    elif planeType == QSR_PlaneType.BACK:
        # Back
        plane = cmds.polyPlane(n='ref_back', w=planeSize, h=planeSize, sx=1, sy=1, ax=(0, 0, 1))
        cmds.setAttr(plane[0]+'.translate', 0, halfSize, (halfSize + planeDistance))
        cmds.setAttr(plane[0]+'.rotate', 0, 180, 0)

    return plane


def QSR_ApplyTexture(mesh, texturePath):
    material = QSR_CreateMaterialFromPath(texturePath)
    cmds.select(mesh[0])
    cmds.hyperShade(assign=material)
    cmds.rename(material, mesh[0]+'_mat')


def QSR_CreateMaterialFromPath(texturePath):
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


def QSR_SearchReferencesInFolder():
    global qsr_planes

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
            qsr_planes[QSR_PlaneType.TOP] = directory+'/'+file
        elif re.search(r'bottom', file):
            qsr_planes[QSR_PlaneType.BOTTOM] = directory+'/'+file
        elif re.search(r'left', file):
            qsr_planes[QSR_PlaneType.SIDE_L] = directory+'/'+file
        elif re.search(r'right', file):
            qsr_planes[QSR_PlaneType.SIDE_R] = directory+'/'+file
        elif re.search(r'front', file):
            qsr_planes[QSR_PlaneType.FRONT] = directory+'/'+file
        elif re.search(r'back', file):
            qsr_planes[QSR_PlaneType.BACK] = directory+'/'+file

    RefreshAllUIImgPath()


def QSR_CreateReferenceLayer():
    # I create the Ref layer once and set it as a reference layer
    if not cmds.objExists('ReferenceLayer'):
        cmds.createDisplayLayer(n='ReferenceLayer', empty=True)
        cmds.setAttr('ReferenceLayer.displayType', 2)


def QSR_AddMeshToReferenceLayer(meshName):
    cmds.editDisplayLayerMembers('ReferenceLayer', meshName)


def QSR_EnableBackfaceCulling(meshName):
    cmds.setAttr(meshName[0]+'.backfaceCulling', 3)


def QSR_GeneratePlanes():
    global qsr_planes

    QSR_CreateReferenceLayer()

    for planeType in qsr_planes:
        plane = QSR_CreatePlane(planeType)
        QSR_ApplyTexture(plane, qsr_planes[planeType])
        QSR_AddMeshToReferenceLayer(plane)
        QSR_EnableBackfaceCulling(plane)


def QSR_FunctionalTest():
    global qsr_planes

    QSR_TestResetHypershade()
    QSR_TestResetScene()
    QSR_TestResetLayers()

    qsr_planes = {
        'top': '/Users/Giorgio/Desktop/TestBlueprints/top.png',
        'bottom': '/Users/Giorgio/Desktop/TestBlueprints/ref_bottom.png',
        'side_l': '/Users/Giorgio/Desktop/TestBlueprints/left.png',
        'side_r': '/Users/Giorgio/Desktop/TestBlueprints/caneright.png',
        'front': '/Users/Giorgio/Desktop/TestBlueprints/front.png',
        'back': '/Users/Giorgio/Desktop/TestBlueprints/img-back.png'
    }

    QSR_GeneratePlanes()


def QSR_InitUI():
    qsr_win_name = 'quick_ref_setup'

    if cmds.window(qsr_win_name, q=True, ex=True):
        cmds.deleteUI(qsr_win_name)

    cmds.window(qsr_win_name, t='Quick References Setup')
    cmds.window(qsr_win_name, e=True, height=100, width=600, sizeable=False)
    cmds.columnLayout(adj=True)

    cmds.intSliderGrp('plane_size', f=True, l='Plane Size', minValue=1, maxValue=10, value=5)
    cmds.intSliderGrp('plane_distance', f=True, l='Plane Distance', minValue=-1, maxValue=10, value=-1)

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Top', c=Callback(QSR_LoadImagePath, QSR_PlaneType.TOP))
    cmds.textField('top_field', w=450)
    cmds.button(label=' X ', c=Callback(QSR_EmptyImgPath, QSR_PlaneType.TOP))
    cmds.setParent('..')

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Bottom', c=Callback(QSR_LoadImagePath, QSR_PlaneType.BOTTOM))
    cmds.textField('bottom_field', w=450)
    cmds.button(label=' X ', c=Callback(QSR_EmptyImgPath, QSR_PlaneType.BOTTOM))
    cmds.setParent('..')

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Left Side', c=Callback(QSR_LoadImagePath, QSR_PlaneType.SIDE_L))
    cmds.textField('side_l_field', w=450)
    cmds.button(label=' X ', c=Callback(QSR_EmptyImgPath, QSR_PlaneType.SIDE_L))
    cmds.setParent('..')

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Right Side', c=Callback(QSR_LoadImagePath, QSR_PlaneType.SIDE_R))
    cmds.textField('side_r_field', w=450)
    cmds.button(label=' X ', c=Callback(QSR_EmptyImgPath, QSR_PlaneType.SIDE_R))
    cmds.setParent('..')

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Front', c=Callback(QSR_LoadImagePath, QSR_PlaneType.FRONT))
    cmds.textField('front_field', w=450)
    cmds.button(label=' X ', c=Callback(QSR_EmptyImgPath, QSR_PlaneType.FRONT))
    cmds.setParent('..')

    cmds.rowLayout(adj=True, nc=3)
    cmds.button(label='Select Back', c=Callback(QSR_LoadImagePath, QSR_PlaneType.BACK))
    cmds.textField('back_field', w=450)
    cmds.button(label=' X ', c=Callback(QSR_EmptyImgPath, QSR_PlaneType.BACK))
    cmds.setParent('..')

    cmds.rowLayout(nc=3)
    cmds.button(label='Remove References', h=50, w=200, c=Callback(QSR_RemoveAllPlaneReferences))
    cmds.button(label='Load from folder', h=50, w=200, c=Callback(QSR_SearchReferencesInFolder))
    cmds.button(label='Generate', h=50, w=200, c=Callback(QSR_GeneratePlanes))
    cmds.setParent('..')
    cmds.showWindow(qsr_win_name)


QSR_InitUI()
# QSR_FunctionalTest()
