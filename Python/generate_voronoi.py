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

# get the object with prefix
my_object = get_all_objects_with_prefix("my")[0]

# initialiing modifiers
init_wireframe_modifier(my_object)
init_subdivision_modifier(my_object)
init_solidify_modifier(my_object)
init_subdivision_modifier(my_object, 3)

# apply all modifiers
apply_all_modifiers(my_object)
