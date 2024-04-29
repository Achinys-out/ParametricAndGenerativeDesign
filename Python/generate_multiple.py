import bpy

WIREFRAME_MODIFIER_NAME = "My Wireframe"
SUBDIVISION_MODIFIER_NAME = "My Subdivision"
SOLIDIFY_MODIFIER_NAME = "My Solidify"
DECIMATE_MODIFIER_NAME = "My Decimate"

# helper - gets all objects with given prefix from the scene
def get_all_objects_with_prefix(prefix):
    all_objects = bpy.context.scene.objects
    return [obj for obj in all_objects if obj.name.startswith(prefix)]

# helper - checks if object obj has given modifier
def get_modifier(obj, modifier_name):
    for m in obj.modifiers:
        if(m.name == modifier_name):
            return m
    return None

# helper - applies all modifiers
def apply_all_modifiers(obj):
    for m in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=m.name)

def init_wireframe_modifier(obj, newThickness=0.1, newOffset=1):
    wireframe_modifier = get_modifier(obj, WIREFRAME_MODIFIER_NAME)
    if(not wireframe_modifier):
        wireframe_modifier = obj.modifiers.new(name=WIREFRAME_MODIFIER_NAME, type='WIREFRAME')
    wireframe_modifier.thickness = newThickness # Thickness         # <0; 1>
    wireframe_modifier.offset = newOffset       # Offset            # <-1; 1>

def init_subdivision_modifier(obj, levels=1):
    subdivision_modifier = obj.modifiers.new(name=SUBDIVISION_MODIFIER_NAME, type='SUBSURF')
    subdivision_modifier.levels = levels        # Levels Viewport   # <0; 6>

def init_solidify_modifier(obj, newThickness=0.1, newOffset=1):
    solidify_modifier = get_modifier(obj, SOLIDIFY_MODIFIER_NAME)
    if(not solidify_modifier):
        solidify_modifier = obj.modifiers.new(name=SOLIDIFY_MODIFIER_NAME, type='SOLIDIFY')
    solidify_modifier.thickness = newThickness  # Thickness         # <-10; 10>
    solidify_modifier.offset = newOffset        # Offset            # <-1; 5>

def init_decimate_modifier(obj, newRatio=1):
    decimate_modifier = get_modifier(obj, DECIMATE_MODIFIER_NAME)
    if(not decimate_modifier):
        decimate_modifier = obj.modifiers.new(name=DECIMATE_MODIFIER_NAME, type='DECIMATE')
    decimate_modifier.ratio = newRatio         # Ratio              # <0; 1>

def duplicate_object(obj):
    collection=bpy.context.collection
    obj_copy = obj.copy()
    obj_copy.data = obj_copy.data.copy()
    collection.objects.link(obj_copy)
    obj_copy.name = obj.name
    return obj_copy

# helper - removes onject completely
def remove_object(obj, unlink=True):
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select the object to be removed
    obj.select_set(True)

    bpy.data.objects.remove(obj, do_unlink=True)

    ## Remove the selected object from the scene
    try:
        bpy.ops.object.delete()
    except:
        pass
    
# Create a cube
bpy.ops.mesh.primitive_cube_add()

# Get the newly created cube
my_object = bpy.context.active_object

# Rename the cube
my_object.name = "my_cube"

# Create array for object copies and put my_object inside
object_copies = [my_object]
    
# Function to generate n copies of object obj (object included)
def generate_objects(obj, n):

    # Copy the object 10 times along the X-axis
    for i in range(1, n):

        # Calculate the radius based on the object's dimensions
        radius = max(obj.dimensions) / 2

        # Initialize amount of spacing between each copy
        spacing = radius + 2.5

        # Duplicate the object
        obj_copy = my_object.copy()
        bpy.context.collection.objects.link(obj_copy)
        obj_copy.data = my_object.data.copy()
        
        # Add new copy of the object into object_copies array
        object_copies.append(obj_copy)

        # Move the duplicated object along the X-axis
        obj_copy.location.x = i * spacing

# Call function to generate 6 copies of my_object
generate_objects(my_object, 6)

init_subdivision_modifier(object_copies[0], 1)
init_subdivision_modifier(object_copies[1], 2)
init_subdivision_modifier(object_copies[2], 3)

init_wireframe_modifier(object_copies[3], newThickness=0.1)
init_wireframe_modifier(object_copies[4], newThickness=0.25)
init_wireframe_modifier(object_copies[5], newThickness=0.4)
