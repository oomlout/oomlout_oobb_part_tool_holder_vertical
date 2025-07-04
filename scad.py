import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    #oomp_mode = "project"
    oomp_mode = "oobb"

    test = False
    #test = True

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
        #default
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
    elif typ == "fast":
        #navigation
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
        #default
        #filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        thickness_extra = 3

        tools = []
        #tool_screwdriver_bit_quarter_inch_drive
        if True:
            tool = {}
            tool["width"] = 9
            tool["height"] = 3
            tool["thickness"] = 9 + thickness_extra
            tool["tool"] = "tool_screwdriver_bit_quarter_inch_drive"
            tool["multiple"] = 8
            tool["spacing"] = 15
            tool["offset_tool"] = [0,-10,0]
            tools.append(tool)
            
            tool2 = copy.deepcopy(tool)
            tool2["multiple"] = 7
            tools.append(tool2)

            tool2 = copy.deepcopy(tool)            
            tool2["layered"] = True
            tools.append(tool2)

            tool = {}
            tool["width"] = 9
            tool["height"] = 4
            tool["thickness"] = 9 + thickness_extra
            tool["tool"] = "tool_screwdriver_bit_quarter_inch_drive"
            tool["multiple"] = 8
            tool["spacing"] = 15
            tool["offset_tool"] = [0,-17.5,0]
            tools.append(tool)
            
            tool2 = copy.deepcopy(tool)
            tool2["multiple"] = 7
            tools.append(tool2)
            
            tool2 = copy.deepcopy(tool)            
            tool2["layered"] = True
            tools.append(tool2)


        for tool in tools:
            part = copy.deepcopy(part_default)
            p3 = copy.deepcopy(kwargs)
            p3.update(tool)
            #p3["width"] = 3
            #p3["height"] = 3
            #p3["thickness"] = 6
            ex = ""
            tool_name = p3["tool"]
            ex += f"{tool_name}_tool"
            multiple = p3.get("multiple", 1)
            if multiple != 1:
                ex += f"_{multiple}_multiple"
            layered = p3.get("layered", False)
            if layered:
                ex += "_layered"
            p3["extra"] = ex
            part["kwargs"] = p3
            nam = "tool_holder_vertical"
            part["name"] = nam
            if oomp_mode == "oobb":
                p3["oomp_size"] = nam
            if not test:
                pass
                parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        sort.append("tool")
        sort.append("multiple")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        sort.append("layered")
        
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    tool = kwargs.get("tool", "")
    multiple = kwargs.get("multiple", 1)
    spacing = kwargs.get("spacing", 15)
    
    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = ["top", "bottom"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_tool_holder_vertical(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", True)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    tool = kwargs.get("tool", "")
    multiple = kwargs.get("multiple", 1)
    spacing = kwargs.get("spacing", 15)
    
    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos) 
    pos1[2] += - depth/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    

    thing = get_tool_cutout(thing, **kwargs)

    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = ["top", "bottom","left"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        #thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += 0
        pos1[2] += -500
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_tool_cutout(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", True)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    tool_name = kwargs.get("tool", "")
    multiple = kwargs.get("multiple", 1)
    spacing = kwargs.get("spacing", 15)
    layered = kwargs.get("layered", False)
    offset_tool = kwargs.get("offset_tool", [0, 0, 0])

    offset_current = [0,0,0]
    offset_current[0] += offset_tool[0] + pos[0]
    offset_current[1] += offset_tool[1] + pos[1]
    offset_current[2] += offset_tool[2] + pos[2]


    tools = {}
    #tool_screwdriver_bit_quarter_inch_drive
    if True:
        tool = {}
        tool["name"] = "tool_screwdriver_bit_quarter_inch_drive"
        #parts
        if True:
            parts = []
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "negative"
            p3["shape"] = f"oobb_cylinder"
            p3["radius"] = 8/2
            dep = 100
            p3["depth"] = dep
            pos = copy.deepcopy(pos)
            pos[0] += 0
            pos[1] += 0
            pos[2] += dep/2
            p3["pos"] = pos
            rot1 = copy.deepcopy(rot)
            rot1[0] += -90
            p3["rot"] = rot1
            #p3["m"] = "#"
            parts.append(p3)
            tool["parts"] = parts
        tools["tool_screwdriver_bit_quarter_inch_drive"] = tool

    


    #add tool
    start_x = -((multiple-1) * spacing) / 2
    for i in range(multiple):
        parts = copy.deepcopy(tools[tool_name]["parts"])
        for part in parts:
            #add spacing
            p3 = copy.deepcopy(part)
            pos1 = copy.deepcopy(offset_current)
            pos_copy = copy.deepcopy(p3["pos"])
            pos1[0] += pos_copy[0] + start_x + (i * spacing)
            pos1[1] += pos_copy[1]
            pos1[2] += pos_copy[2]
            
            p3["pos"] = pos1
            oobb_base.append_full(thing, **p3)

    #add layered
    if layered:
        multiple = multiple - 1
        start_x = -((multiple-1) * spacing) / 2
        for i in range(multiple):
            parts = copy.deepcopy(tools[tool_name]["parts"])
            for part in parts:
                #add spacing
                p3 = copy.deepcopy(part)
                pos1 = copy.deepcopy(offset_current)
                pos_copy = copy.deepcopy(p3["pos"])
                pos1[0] += pos_copy[0] + start_x + (i * spacing)
                pos1[1] += pos_copy[1]
                pos1[2] += pos_copy[2] + depth / 2
                
                p3["pos"] = pos1
                oobb_base.append_full(thing, **p3)



    return thing


if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)