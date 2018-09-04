# maya-tools

Maya scripts I made in order to speed up my workflow

# How to load scripts on Maya

* Open Maya (whatever version is fine)
* Click on the [small button with a semicolumn](screenshots/MayaScriptEditorButton.png?raw=true) on the lower-right edge of the screen
* On the [new window that has been opened](screenshots/MayaScriptEditor.png?raw=true) and click on File > Load script
* Click on the [ExecuteAll button](screenshots/MayaExecuteAllButton.png?raw=true) (the icon that looks like a fast-forward button)

# How to use the scripts

## boolean_utilities.py

#### Does a boolean intersection and preserves the two intersectated meshes

* Run the script
* Press the button **difference + intersection** or
* Press the button **intersection (preserve meshes)**

## chain_maker.mel _(deprecated, needs to be rewritten in Python)_

## clean_export_routine.py

#### Merges all the meshes, sets pivot in the bottom center, freezes transforms and deletes history

* Run the script
* Export the model

## even_selection.py

#### Given a selection, it deselects the odd elements

* Select any number of faces, vertices or edges
* Run the script
* You should have only the even elements selected

## quick_references_setup.py

#### Loads and positions reference images on the scene automatically

* Run the script
* Add references images manually
* Alternatively, you can select a folder containing them by pressing **load from folder** button
* Press the **generate** button
* When you're done, press the button **remove references**

## quick_texture_material.py

#### Quickly creates a new material from an image

* Run the script
* Select the image that you want to put on the material
* You should have a material with the image you have chosen

## randomizer.mel _(deprecated, needs to be rewritten in Python)_
