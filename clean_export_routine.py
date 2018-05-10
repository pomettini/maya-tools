# coding=utf-8

'''
	Funzione che centra il pivot nel vertice più basso
	mette il modello a posizione 0, freeza la transform 
	e cancella la storia
'''

import maya.cmds as cmds
import random

# TEST Reset the scene to the original state
def TestReset():
	cmds.select(all=True)
	cmds.delete()

# TEST Create a sphere and triangulate it
def TestCreate():
	cmds.polySphere(name='Object001')
	cmds.polyTriangulate('Object001', ch=True)

# TEST Create multiple spheres, merge them, apply triangulate
def TestCreateMultiple():
	cmds.polySphere(name='Object001')
	cmds.move(-0.5, -1, -0.5, 'Object001')
	cmds.polySphere(name='Object002')
	MergeAllMeshes()
	cmds.polyTriangulate('FinalModel', ch=True)

#TEST Create multiple objects at random positions, merge them, apply triangulate
def TestCreateMultipleRandom():
	for i in range(0, 30):
		cmds.polySphere(name='Object'+str(i))
		cmds.move(random.randint(-4, 4), random.randint(-3, 3), random.randint(-2, 2), 'Object'+str(i))
	MergeAllMeshes()
	cmds.polyTriangulate('FinalModel', ch=True)

def MergeAllMeshes():
	# Select all meshes
	cmds.select(all=True)
	# Put the selection to an array
	selection = cmds.ls(sl=True)
	# If you have at least two objects, it merges them
	if len(selection) > 1:
		cmds.polyUnite(*selection, name='FinalModel')

def SetPivotToBottomCenter():
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

def FreezeTransforms():
	cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)

def DeleteHistory():
	selection = cmds.ls(sl=True)
	# Delete the history of every object selected
	for obj in selection:
		cmds.delete(obj, ch=True)

def FunctionalTest1():
	TestReset()
	TestCreate()
	SetPivotToBottomCenter()
	FreezeTransforms()
	DeleteHistory()

def FunctionalTest2():
	TestReset()
	TestCreateMultiple()
	SetPivotToBottomCenter()
	FreezeTransforms()
	DeleteHistory()

def FunctionalTest3():
	TestReset()
	TestCreateMultipleRandom()
	SetPivotToBottomCenter()
	FreezeTransforms()
	DeleteHistory()

def CleanExportRoutine():
	MergeAllMeshes()
	SetPivotToBottomCenter()
	FreezeTransforms()
	DeleteHistory()

#TestReset()
#FunctionalTest1()
#FunctionalTest2()
#FunctionalTest3()
CleanExportRoutine()