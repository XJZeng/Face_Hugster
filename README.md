# Face_Hugster

How to use:

Save Selection Module:

    #This module allows the user to save a wide range of selection into the manager. User can select vertices, 
    #edges, UVs, different geometries, etc.
    
    1)  Selection Manager:
        - Make a selection and use the save button to name and save into the manager. 
        - Click on the name to select the selection set.
        - to delete, click on the name and press the delete key, or use Clear Selection button for all.
        
    2)  Save Selection to File:
        - Saves everything in the selection manager to a text file where your Maya scene is located.
        - To reload the selection, press the load selection button.
        ** - will not work if the Maya file is not saved onto disk.
        
Duplicate From Selection Module:

    #This module allows the user to make a copy of the selected faces into a new geometry. 
    #It duplicates the geometry, renames it, copies the selection, and delete the unselected faces. 
    #If geometry is dense, this will be take time.
    
    1) Duplicate Selection:
        - Select a list from the Selection Manager and click on the button to make a duplicate geometry
          from the selection.
          
Palette Manager Module:

    #This module allows the user to add the geometry to be copied into a list.

    1)  Palette Manager:
        - Select the geometry to be copied and click on Set To Palette to put into the Palette Manager.
        - to delete, click on the name and press the delete key or use Clear Palette for all.
        ** For best results, set a good pivot point. Do not freeze translation transform or geometry
           will not be at correct position.

Run Module:

    #Runs the tool as either instances or duplicates.

    1)  Run Command:
        - To run the tool, please do the following:
           1) Select a list from the Selection Manager that you wish to populate.
           2) Click on a geometry that you wish to copy.
           3) Select whether you want to run as instances or duplicates. Default is duplicate.
           4) Hit run button.
           ** Will not work if face selection is not active in viewport, so remember to 
              select from Selection Manager before running.
              
Rotate Constraint Module:

    #This module allows the user to orient constraint all geometries under a selected group to a locator. 
    #This allows the user flexibility in rotating multiple geometries with one control.
          
    1)  Constrain Geometry:
        - Select the group node and click the button.
        
    2)  Rehook Constrain:
        - This allows the user to re-orient geometries to a previously set locator
          (group name and locator name must match).
      
    3)  Break Constrain:
        - Deletes the constrains after rotation is done. 
          
          


