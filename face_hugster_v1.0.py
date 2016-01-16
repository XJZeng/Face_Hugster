import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import os, string, math, re
from os import path, listdir, rename
from string import Template, zfill
from functools import partial

FACE_CENTER_DICT={}
SAVE_SELECTION_DICT={}

class Face_Center:
    def __init__(self):
        # This finds the face center of each face and uploads data to the global dictionary
        face_center = []

        selection = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(selection)

        iter_sel = OpenMaya.MItSelectionList (selection, OpenMaya.MFn.kMeshPolygonComponent)

        while not iter_sel.isDone():
            dag_path = OpenMaya.MDagPath()
            component = OpenMaya.MObject()

            iter_sel.getDagPath(dag_path, component)

            poly_iter = OpenMaya.MItMeshPolygon(dag_path, component)

            while not poly_iter.isDone():
                # enumerates the faces in selection
                i = 0
                i = poly_iter.index()
                face_info = ("face %s" %i)
                
                # finds the face center of enumerated face                
                center = OpenMaya.MPoint
                center = poly_iter.center(OpenMaya.MSpace.kWorld)
                point = [0.0,0.0,0.0]
                point[0] = center.x
                point[1] = center.y
                point[2] = center.z
                face_center = point
                
                # uploads face to global dictionary
                FACE_CENTER_DICT.update({face_info:face_center})
                
                #goes to next face
                poly_iter.next()
                
            iter_sel.next()
                   
class Save_To_File:
    def __init__(self, dir_path, maya_file, write_file_name, sel_list):
        ##specify file directory file name to be saved        
        self.dir_path = dir_path 
        self.maya_file = maya_file       
        self.file_name = write_file_name
        
        ##selection to be saved
        self.sel_list = sel_list        
        to_write_list = []
        
        for dummy_selection in self.sel_list:            
            for dummy_key, dummy_val in SAVE_SELECTION_DICT.iteritems():
                if dummy_selection == dummy_key:
                    ##format setup
                    dummy_selection_name = dummy_selection + ' = '
                    dummy_base_template = dummy_selection_name + ' _placeholder_ '
                    ##the string that joins the individual values in the list together
                    dummy_line_join = ', '
                    ##the join function
                    dummy_list_to_text = dummy_line_join.join(dummy_val)
                    ##generating the text to be written
                    if '_placeholder_' in dummy_base_template:
                        dummy_print_to_text = dummy_base_template.replace('_placeholder_', dummy_list_to_text)
                        to_write_list.append(dummy_print_to_text+'\r\n')
        ##writing to file
        file_open = open(self.dir_path+ '\\' + self.file_name, 'w+')
        file_open.writelines(to_write_list)
        file_open.close()
                            

class Mass_Planter:
    
    def __init__(self, root_obj_name, sel_name, run_option):
        # this function runs the script
        face_sel = cmds.ls(sl=True, fl=True) # makes a selection from the UI
        Face_Center()# passes the selection into Face_Center class to find centers of faces in face_sel
        self.run_option = run_option
        self.sel_name = sel_name
        self.dupe_geo_list = []
        for dummy_item in face_sel:                        
            for key, val in FACE_CENTER_DICT.iteritems(): # loops through global dict to find relevant coordinates
                if self.run_option == 'Instance':
                    dummy_new_geo = cmds.instance(root_obj_name)
                elif self.run_option == 'Duplicate':
                    dummy_new_geo = cmds.duplicate(root_obj_name)
                cmds.setAttr( str(dummy_new_geo[0])+'.translateX', val[0] )
                cmds.setAttr( str(dummy_new_geo[0])+'.translateY', val[1] )
                cmds.setAttr( str(dummy_new_geo[0])+'.translateZ', val[2] )
                dummy_constr = cmds.normalConstraint(dummy_item, str(dummy_new_geo[0]), aimVector = (0,1,0), u = (0,1,0), worldUpType= 0, wu = (0, 1, 0))
                cmds.delete(dummy_constr)
                self.dupe_geo_list.append(dummy_new_geo)
            cmds.setAttr( str(root_obj_name)+'.translateX', 0 )
            cmds.setAttr( str(root_obj_name)+'.translateY', 0 )
            cmds.setAttr( str(root_obj_name)+'.translateZ', 0 )
            cmds.setAttr( str(root_obj_name)+'.rotateX', 0 )
            cmds.setAttr( str(root_obj_name)+'.rotateY', 0 )
            cmds.setAttr( str(root_obj_name)+'.rotateZ', 0 )               
            FACE_CENTER_DICT.clear() # memory management purposes 
        self.sel_name_grp=cmds.group( em=True, name=self.sel_name ) # creates a group to house the duplicated geometries
        for dummy_geo in self.dupe_geo_list:
            cmds.parent( dummy_geo, str(self.sel_name_grp) )                


class Mass_Planter_UI:
    def __init__(self, *args):
        # UI for script
        self.run_option = 'Duplicate'
        self.bin_loc = None
        self.bin_file = None
        window = cmds.window( title="Face Hugster", iconName='FceHug', w=280, h=220, s = True )   
        cmds.columnLayout( adjustableColumn=True, rowSpacing=10)
                
        cmds.frameLayout( label='Selection Manager', borderStyle='in', cll=True, cl=True )
        cmds.text( label='Save Your Selection:', align='left' )
        self.scroll_box=cmds.textScrollList( numberOfRows=6, w = 250, h = 80, selectCommand=partial(self.select_from_list, 1),
                deleteKeyCommand = partial(self.delete_selection, 1) )
        cmds.button( label='Save Selection', command=partial(self.save_selection, 1) )
        cmds.button( label='Clear All Selection', command=partial(self.clear_all_selection, 1) )
        cmds.separator( style='single' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.frameLayout( label='Save And Load To File', borderStyle='in', cll=True, cl=True )
        cmds.text( label='', align='left' ) 
        cmds.button( label='Save Selection To File', command=partial(self.save_to_file, 1) )
        cmds.button( label='Load Selection', command=partial(self.load_file, 1) )
        cmds.separator( style='single' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.frameLayout( label='Duplicate Geometry From Selection', borderStyle='in', cll=True, cl=True )
        cmds.text( label='', align='left' )        
        cmds.button( label='Duplicate Selection', command=partial(self.duplicate_selection, 1) )
        cmds.separator( style='single' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )        

        cmds.frameLayout( label='Palette Manager', borderStyle='in', cll=True, cl=True )        
        cmds.text( label='Add Geometry to palette:', align='left' )
        self.palette_box=cmds.textScrollList( numberOfRows=6, w = 250, h = 80, selectCommand=partial(self.select_from_palette, 1),
                deleteKeyCommand = partial(self.delete_from_palette, 1) )
        cmds.button( label='Set To Palette', command=partial(self.set_palette_obj, 1) )
        cmds.button( label='Clear Palette', command=partial(self.clear_palette_obj, 1) )
        cmds.separator( style='single' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )          

        cmds.frameLayout( label='Run Face Hugster', borderStyle='in', cll=True, cl=True )        
        cmds.text( label='Run Command:', align='left' )
        cmds.radioButtonGrp( label='Duplicate Type:', labelArray2=['Instance', 'Copy'], 
                numberOfRadioButtons=2, cw3 =[85, 85, 85], cal = [1, 'left'], on1=partial(self.option_instance, 1)
                                , on2=partial(self.option_copy, 1) )    
        cmds.button( label='Run', command=partial(self.run_command, 1) )
        cmds.separator( style='single' )        
        cmds.setParent( '..' )
        cmds.setParent( '..' )           


        cmds.frameLayout( label='Rotation Constrain', borderStyle='in', cll=True, cl=True )        
        cmds.text( label='Constrains selected geometries to locator:', align='left' )   
        cmds.button( label='Constrain geometry', command=partial(self.constrain_geometry, 1) )
        cmds.button( label='Rehook Constrain', command=partial(self.rehook_constrain, 1) )
        cmds.button( label='Break Constrain', command=partial(self.break_constrain, 1) )
        cmds.separator( style='single' )        
        cmds.setParent( '..' )
        cmds.setParent( '..' )           
        
        
        cmds.setParent( '..' )
        cmds.showWindow( window )

    def save_selection(self, *args):
        # make save selection ala 3DS Max. Can save other selection types such as edges or vertices 
        sel_list = cmds.ls(sl=True, fl=True)
        selection_name = str(raw_input('Selection Name: '))
        SAVE_SELECTION_DICT[selection_name] = sel_list
        cmds.textScrollList(self.scroll_box, edit=True, append=selection_name)
        
    def select_from_list(self, *args):
        # runs the cmds.select command for the core script to run
        list_name = cmds.textScrollList(self.scroll_box, query=True, selectItem=True)
        cmds.select(SAVE_SELECTION_DICT[list_name[0]])
    
    def delete_selection(self, *args):
        # deletes selection from list on command
        list_name = cmds.textScrollList(self.scroll_box, query=True, selectItem=True)
        cmds.textScrollList(self.scroll_box, edit=True, ri=list_name[0])
        SAVE_SELECTION_DICT.pop(list_name[0], None)
        
            
    def clear_all_selection(self, *args):
        # memory management. Highly recommended to run this before running another instance of the script or when task is done
        SAVE_SELECTION_DICT.clear()
        cmds.textScrollList(self.scroll_box, edit = True, removeAll=True)
    
    def save_to_file(self, *args):
        
        file_name = cmds.file(q=True, sn=True, shn=True)#maya file name
        file_loc = re.sub(file_name, '', cmds.file(q=True, loc=True))#maya file location
        if not os.path.exists(file_loc + 'FceHug_bin'):
            os.makedirs(file_loc + 'FceHug_bin')
        if not os.path.exists(file_loc + 'FceHug_bin' + '\\Save_Selection_For' + '_' + re.sub('.ma', '',file_name) +'.txt'):
           open(file_loc + 'FceHug_bin' + '\\Save_Selection_For' + '_' + re.sub('.ma', '',file_name) +'.txt', 'w+')
        
        self.bin_loc = file_loc + 'FceHug_bin'
        self.bin_file = 'Save_Selection_For' + '_' + re.sub('.ma', '', file_name) +'.txt'
        
        list_of_selection = cmds.textScrollList(self.scroll_box, query=True, ai=True)
        Save_To_File( self.bin_loc, file_name, self.bin_file, list_of_selection)            
        
    def load_file(self, *args):
        file_name = cmds.file(q=True, sn=True, shn=True)#maya file name
        file_loc = re.sub(file_name, '', cmds.file(q=True, loc=True))#maya file location
        self.bin_loc = file_loc + 'FceHug_bin'
        self.bin_file = 'Save_Selection_For' + '_' + re.sub('.ma', '', file_name) +'.txt'        
        file_open = open( self.bin_loc + '\\' + self.bin_file, 'r')
        content_list = file_open.readlines()
        
        ##loop to analyse and break the txt file and upload to global SAVE_SELECTION_DICT
        for dummy_file in content_list:
            dummy_holding_list = []#for holding face information
            slice_point = dummy_file.find(' = ')
            list_dict_key = dummy_file[:slice_point]#finding variable name/key
            list_dict_val = dummy_file[slice_point+3:].split()#gets the list
            for dummy_item in list_dict_val:
                ## seperating out the junk stuff from the ***.split() action
                if dummy_item == '[' or dummy_item == ']': #the brackets got split too
                    pass
                elif ',' in dummy_item:#all the variables except the last one has a dumbfuck comma behind it
                    dummy_new_item = re.sub(',', '', dummy_item)# removing the comma
                    dummy_holding_list.append(dummy_new_item)
                else:
                    dummy_holding_list.append(dummy_item)
            SAVE_SELECTION_DICT[str(list_dict_key)] = dummy_holding_list #uploading to global dict
            cmds.textScrollList(self.scroll_box, edit=True, append=list_dict_key)
                
    def duplicate_selection(self, *args):
        sel_list = cmds.ls(sl=True, fl = True)
        if len(sel_list) >= 1:
            slice_point = sel_list[0].find('.')
            geo_name = sel_list[0][:int(slice_point)]
        else:
            print 'Need a Selection'
            pass
        duplicate_geo_name = cmds.textScrollList(self.scroll_box, query=True, selectItem=True)
        duplicate_geo = cmds.duplicate(geo_name, n=duplicate_geo_name[0] + '_geo_copy')
        
        duplicate_geo_face_list = []
        
        for dummy_face in sel_list:
            new_face_name=re.sub(geo_name, duplicate_geo[0], dummy_face)
            duplicate_geo_face_list.append(new_face_name)
         
        cmds.select(duplicate_geo_face_list)
        mel.eval('InvertSelection')
        cmds.delete()
    
    def select_from_palette(self, *args):
        # select the target object to be duplicated
        palette_obj_name = cmds.textScrollList(self.palette_box, query=True, selectItem=True)
        return palette_obj_name[0]            
    
    def delete_from_palette(self, *args):
        palette_obj_name = cmds.textScrollList(self.palette_box, query=True, selectItem=True)
        cmds.textScrollList(self.palette_box, edit=True, ri=palette_obj_name[0])
    
    def set_palette_obj(self, *args):
        # puts the target object(s) into a palette for convienient usage
        palette_list = cmds.ls(sl=True, fl=True)
        for dummy_palette_obj in palette_list:
            cmds.textScrollList(self.palette_box, edit=True, append=dummy_palette_obj)
    
    def clear_palette_obj(self, *args):
        # clears the palette of all options
        cmds.textScrollList(self.palette_box, edit=True, ra=True)
            
    def option_instance(self, *args):
        # tells the script to duplicate instances
        self.run_option = 'Instance'
        print self.run_option
        
    def option_copy(self, *args):
        # tells the script to run standard duplication
        self.run_option = 'Duplicate'
        print self.run_option
    
    def constrain_geometry(self, *args):
        run_list = cmds.ls(sl=True, fl=True)
        
        for dummy_list in run_list:
            dummy_geo_list = cmds.listRelatives(dummy_list, c=True)
            dummy_locator = cmds.spaceLocator(n = dummy_list+'_constrain')
            #dummy_logo = cmds.textCurves( f='Times-Roman|h-1|w-400|c0', o = True, t=dummy_list + '_control' )
            #cmds.parent( dummy_logo, dummy_locator, add=True )
            for dummy_geo in dummy_geo_list:
                cmds.orientConstraint( dummy_locator, dummy_geo )
    
    def rehook_constrain(self, *args):
        group_sel = cmds.ls(sl=True, fl=True)
        
        for dummy_group in group_sel:
            locator_name = str(dummy_group) + '_constrain'
            dummy_geo_list = cmds.listRelatives(dummy_group, c=True)
            for dummy_geo in dummy_geo_list:
                cmds.orientConstraint( locator_name, dummy_geo )
            
    
    def break_constrain(self, *args):
        group_sel = cmds.ls(sl=True, fl=True)
        
        for dummy_group in group_sel:
            dummy_geo_list = cmds.listRelatives(dummy_group, c = True) or []
            for dummy_geo in dummy_geo_list:
                attr_list = cmds.listRelatives(dummy_geo) or []
                for attr in attr_list:
                    if 'orientConstraint' in attr:
                        cmds.delete(attr)
                
        

    def run_command(self, *args):
        # runs the core script
        self.list_name = cmds.textScrollList(self.scroll_box, query=True, selectItem=True) # query name list for creating relevant group name
        print 'Planting selection -- ' + self.list_name[0] + ' | with geometry -- ' + str(self.select_from_palette()) #+ ' as ' + self.run_option
        Mass_Planter(self.select_from_palette(), self.list_name[0], self.run_option)
                  
def main():

        Mass_Planter_UI()

if __name__=='__main__':
	main()


