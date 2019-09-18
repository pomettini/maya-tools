# coding=utf-8

'''
	Centers the pivot in the lowest vertex
	Puts the model in the bottom, freezes transform
	And deletes history
'''

import maya.cmds as cmds
import random

# TEST Reset the scene to the original state
def CER_TestReset():
	cmds.select(all=True)
	cmds.delete()

# TEST Create a sphere and triangulate it
def CER_TestCreate():
	cmds.polySphere(name='Object001')
	cmds.polyTriangulate('Object001', ch=True)

# TEST Create multiple spheres, merge them, apply triangulate
def CER_TestCreateMultiple():
	cmds.polySphere(name='Object001')
	cmds.move(-0.5, -1, -0.5, 'Object001')
	cmds.polySphere(name='Object002')
	CER_MergeAllMeshes()
	cmds.polyTriangulate('FinalModel', ch=True)

#TEST Create multiple objects at random positions, merge them, apply triangulate
def CER_TestCreateMultipleRandom():
	for i in range(0, 30):
		cmds.polySphere(name='Object'+str(i))
		cmds.move(random.randint(-4, 4), random.randint(-3, 3), random.randint(-2, 2), 'Object'+str(i))
	CER_MergeAllMeshes()
	cmds.polyTriangulate('FinalModel', ch=True)

def CER_MergeAllMeshes():
	# Select all meshes
	cmds.select(all=True)
	# Put the selection to an array
	selection = cmds.ls(sl=True)
	# If you have at least two objects, it merges them
	if len(selection) > 2:
		cmds.polyUnite(*selection, name='FinalModel')

def CER_SetPivotToBottomCenter():
	# Gets the selected object
	selection = cmds.ls(sl=True)
	# Gets the bounding box of the object
	bbox = cmds.exactWorldBoundingBox(selection[0])
	# Gets the middle bottom part of the bounding box
	bottom = [(bbox[0]+bbox[3])/2, bbox[1], (bbox[2]+bbox[5])/2]
	# Sets the pivot in that point
	cmds.xform(selection, piv=bottom, worldSpace=True)
	# Moves the mesh to the world origin
	cmds.move(0, 0, 0, selection[0], rpr=True)

def CER_FreezeTransforms():
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)

def CER_DeleteHistory():
	selection = cmds.ls(sl=True)
	# Delete the history of every object selected
	for obj in selection:
		cmds.delete(obj, ch=True)

def CER_FunctionalTest1():
	CER_TestReset()
	CER_TestCreate()
	CER_SetPivotToBottomCenter()
	CER_FreezeTransforms()
	CER_DeleteHistory()

def CER_FunctionalTest2():
	CER_TestReset()
	CER_TestCreateMultiple()
	CER_SetPivotToBottomCenter()
	CER_FreezeTransforms()
	CER_DeleteHistory()

def CER_FunctionalTest3():
	CER_TestReset()
	CER_TestCreateMultipleRandom()
	CER_SetPivotToBottomCenter()
	CER_FreezeTransforms()
	CER_DeleteHistory()

def CER_CleanExportRoutine():
	CER_MergeAllMeshes()
	CER_SetPivotToBottomCenter()
	CER_FreezeTransforms()
	CER_DeleteHistory()

# CER_TestReset()
# CER_FunctionalTest1()
# CER_FunctionalTest2()
# CER_FunctionalTest3()
CER_CleanExportRoutine()
