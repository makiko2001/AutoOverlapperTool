#Maggie Vichitudomchock
"""Auto Overlapping tool for animation
Users must animate base animation before running the tool.
"""

import maya.cmds as cmds
        
#----------#
#UI part

def delete_ui(window_name):
    if cmds.window(window_name, exists = True):
        cmds.deleteUI(window_name)
        
def main():
    window_name = "Auto_Overlapping_Tool"
    delete_ui(window_name)
    cmds.window(window_name, resizeToFitChildren= True , widthHeight=(250, 200))
    main_layout = cmds.rowColumnLayout()
    
    cmds.separator(style = "none", height = 5)
    cmds.text("Auto Overlapping Tool", font = "boldLabelFont", parent = main_layout)    
    cmds.text("Maggie Vichitudomchock", font = "fixedWidthFont", parent = main_layout)
    cmds.separator(style = "none", height = 5)
    
    #selecting frames for overlapping
    frame_layout = cmds.rowColumnLayout(numberOfColumns = 4, columnWidth = [(1, 200), (2, 75), (3,20), (4,75)], parent = main_layout, bgc = (0.5, 0.5, 0.5))
    
    cmds.text("Start Frame - End Frame", parent = frame_layout)
    start_frame_int = cmds.intField(value = 0, parent = frame_layout)
    cmds.separator(style = "none", horizontal = False, parent = frame_layout)
    end_frame_int = cmds.intField(value = 10, parent = frame_layout)
    
    #Attributes Selection
    rb_layout = cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [(1,110), (2, 350)], parent = main_layout)
    attribute_list = []
    
    global axis_rb
    cmds.text("Rotate : ")
    axis_rb = cmds.radioButtonGrp(labelArray3=['X', 'Y', 'Z'],
                                  numberOfRadioButtons=3, parent=rb_layout, select = 2)
    
    
    cmds.separator(style = "none", height = 5, parent = rb_layout)
    cmds.separator(style = "none", height = 5, parent = rb_layout)
    
    #Motion selection
    global cycle_rb
    cmds.text("Motion : " )                             
    cycle_rb = cmds.radioButtonGrp(labelArray3=['Cycle', 'Oscillate', 'Constant'],
                                  numberOfRadioButtons=3, parent=rb_layout, select = 1)
    
    #Separator
    cmds.separator(style = "single", height = 25, width = 250, parent = rb_layout)
    cmds.separator(style = "single", height = 25, width = 250, parent = rb_layout)
    
    #Offset input
    offset_layout = cmds.rowColumnLayout(numberOfColumns = 4, width = 500, columnWidth = [(1,100), (2, 75), (3,100), (4, 75)], parent = main_layout)
    cmds.text("Offset", parent=offset_layout)                             
    offset_int_field = cmds.intField(value=2, parent=offset_layout)
    
    cmds.text("Amplitude", parent = offset_layout)
    amplitude_float_field = cmds.floatField(value = 1, parent= offset_layout)
    
    #Button 
    button_layout = cmds.rowColumnLayout(numberOfColumns = 4, width = 300, columnWidth = [(1,75), (2,100),(3,25), (4,100)])
    
    cmds.separator(style = "none", height = 25, width = 250, parent = button_layout)
    btn1 = cmds.button(label = "Overlap", parent = button_layout, command = lambda*args:get_inputs(offset_int_field, amplitude_float_field, start_frame_int, end_frame_int), bgc = (0.7,1,0.7 ))    
    cmds.separator(style = "none", height = 25, width = 250, parent = button_layout)
    btn2 = cmds.button(label = "Cancel", parent = button_layout, command = lambda*args:delete_ui(window_name), bgc = (0.98,0.39,0.39))
    
    cmds.showWindow(window_name)

#----------#
#code

#store user selection into a list, recall later in overlap()
def get_user_selection():
    axis_selection = cmds.radioButtonGrp(axis_rb, query=True, select=True)

    attribute_list = ["rotate", "Y"]

    if axis_selection == 1:
        attribute_list[1] = ("X")
    elif axis_selection == 2:
        attribute_list[1] = ("Y")
    elif axis_selection == 3:
        attribute_list[1] = ("Z")
    
    global attribute_combine
    attribute_combine = attribute_list[0]+attribute_list[1]
    
    print(attribute_combine)
    

#main part of the code    
def overlap(offset_int_field, amplitude_float_field, start_frame_int, end_frame_int):
    offset_size = cmds.intField(offset_int_field, query= True, value = True)
    amplitude_size = cmds.floatField(amplitude_float_field, query= True, value = True)
    start_frame = cmds.intField(start_frame_int, query = True, value = True)
    end_frame = cmds.intField(end_frame_int, query = True, value = True)
    
    #User select a control
    base_ctrl = cmds.ls(selection = True, type = "transform")
    
    if not base_ctrl:
        cmds.warning("Please select a control.")
        return
    
    #select hierarchy to find children controls
    descendents_ctrls = cmds.listRelatives(base_ctrl, allDescendents = True)
    
    if not base_ctrl:
        cmds.warning("No child controls found.")
        return
    
    #ignore shapes and store transforms into group
    children_ctrls = []
    for descendents_ctrl in descendents_ctrls:
        if "Shape" not in descendents_ctrl:
            children_ctrls.append(descendents_ctrl)
    
    print(children_ctrls)
    
    children_ctrls.sort()
#-----
    #store all keyframes in a list
    keyframes_in_range = list(range(start_frame, end_frame + 1))
        
    print(keyframes_in_range)
            
    #find first keyframe, then store in list
    base_ctrl_keys = []
    base_ctrl_key = cmds.findKeyframe( base_ctrl , time=(keyframes_in_range[0], keyframes_in_range[0]), attribute = attribute_combine, which = "first")
    base_ctrl_keys.append(base_ctrl_key)
    
    #find the rest of the keyframes using first keyframe as reference, store in list
    for frame in keyframes_in_range[1:]:
        base_ctrl_key = cmds.findKeyframe( base_ctrl , time=(frame, frame), attribute = attribute_combine, which = "next")
        if base_ctrl_key not in base_ctrl_keys and base_ctrl_key in keyframes_in_range:
            base_ctrl_keys.append(base_ctrl_key)
    
            print(base_ctrl_keys)
            
            #get selected attribute value for all base_ctrl_keys
            base_ctrl_attrs = []
            for key in base_ctrl_keys:
                base_ctrl_attr = cmds.getAttr(f"{base_ctrl[0]}.{attribute_combine}", time = key)
                base_ctrl_attrs.append(base_ctrl_attr)
            
            print(base_ctrl_attrs)
            
            #for i in range, (i * amplitude_size) to store value for amplitude of each keys
            amplitudes = []
            
            for i in range(len(base_ctrl_attrs)):
                amplitude = (base_ctrl_attrs[i])*(amplitude_size)
                amplitudes.append(amplitude)
            
            print(amplitudes)
#----
                
    if "rotate" in attribute_combine:
        #cmds.copyKey from base_ctrl
        cmds.copyKey(base_ctrl, time = (start_frame , end_frame), attribute = attribute_combine)
        
        #assign which radio button mean which cycle
        pre_infinite = "cycle"
        post_infinite = "cycle"
        if cmds.radioButtonGrp(cycle_rb, query=True, select=True) == 2:
            pre_infinite = "oscillate"
            post_infinite = "oscillate"
        elif cmds.radioButtonGrp(cycle_rb, query=True, select=True) == 3:
            pre_infinite = "constant"
            post_infinite = "constant"
            parent_ctrl = cmds.listRelatives(allParents = True, type = "transform")
            all_ctrls = base_ctrl + parent_ctrl
            cmds.setInfinity(all_ctrls, preInfinite = "constant", postInfinite = "constant")
        
        #cmds.pasteKey with offset and set Cycle
        for children_ctrl in children_ctrls:          
            cmds.pasteKey(children_ctrl, attribute = attribute_combine, timeOffset = offset_size)
            cmds.setInfinity(children_ctrl, preInfinite = pre_infinite, postInfinite = post_infinite)
            
            #count the amount of keyframes and store it into the list which will be used as index
            number_of_keyframes = cmds.keyframe(f"{children_ctrl}.{attribute_combine}", query=True, keyframeCount=True )
            print(f"number_of_keyframes is {number_of_keyframes}")
            
            index_of_keyframes = list(range(0, number_of_keyframes -1))
            
            print(f"index_of_keyframes is {index_of_keyframes}")
            
            for index_of_keyframe in index_of_keyframes:
               cmds.selectKey(f"{children_ctrl}.{attribute_combine}", t = (index_of_keyframe, index_of_keyframe))
               cmds.keyframe(f"{children_ctrl}.{attribute_combine}", edit=True, absolute = True, index = (index_of_keyframe, index_of_keyframe), valueChange = amplitudes[index_of_keyframe])
               print(amplitudes[index_of_keyframe])
                
            #find new start frame and end frame
            start_frame = start_frame + offset_size
            end_frame = end_frame + offset_size
            
            cmds.copyKey(children_ctrl, time = (start_frame,end_frame), attribute = attribute_combine)
   
#---------#
#controllers
def get_inputs(offset_int_field, amplitude_float_field, start_frame_int, end_frame_int):
    get_user_selection()
    overlap(offset_int_field, amplitude_float_field, start_frame_int, end_frame_int)
    
main()