import bpy
import numpy as np
import bmesh
# NSGAIII currently only works on minimization problems
# MOEAD takes too long to calculate
from platypus import Problem, Real, NSGAII, MOEAD, NSGAIII
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============== CONSTANTS ============== #
WIREFRAME_MODIFIER_NAME = "Wireframe"
SUBDIVISION_MODIFIER_NAME = "Subdivision"
SOLIDIFY_MODIFIER_NAME = "Solidify"
DECIMATE_MODIFIER_NAME = "Decimate"
FITNESS_RANGE = 100 # we want to normalize all fitness functions results to be within <0,100>
        
# Checks if object obj has given modifier
def get_modifier(obj, modifier_name):
    for m in obj.modifiers:
        if(m.name == modifier_name):
            return m
    return None

# Applies all modifiers
def apply_all_modifiers(obj):
    bpy.context.view_layer.objects.active = obj
    for m in obj.modifiers:
        try:
            bpy.ops.object.modifier_apply(modifier=m.name)
        except:
            pass

# helper - gets all objects with given prefix from the scene
""" 
bpy.context.scene.objects: 
This gives you access to the objects that are currently part of the active scene. 
It provides a reference to the objects in the specific scene that is currently active in the context.

bpy.data.objects: This provides access to all objects in the Blender data block regardless of whether 
they are currently in the scene or not. It gives you access to objects that are defined in the .blend 
file, including objects that may not be currently visible or active in any scene.
"""
def get_all_objects_with_prefix(prefix):
    #all_objects = bpy.context.scene.objects
    all_objects = bpy.data.objects
    return [obj for obj in all_objects if obj.name.startswith(prefix)]

# helper - removes onject completely
def remove_object(obj, unlink=True):
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select the object to be removed
    obj.select_set(True)

    # Unlinks and removes the object
    bpy.data.objects.remove(obj, do_unlink=True)

# helper - duplicates object
def duplicate_object(obj):
    collection=bpy.context.collection
    obj_copy = obj.copy()
    obj_copy.data = obj_copy.data.copy()
    collection.objects.link(obj_copy)
    obj_copy.name = obj.name
    return obj_copy

# helper - removes redundant double verices from object 
#  (can be used for better faces or surface area calculation)
def remove_redundant_vertices(object):
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')

# helper - sets object mode to "Object Mode" so we can modify and evaluate it in fitness function
def set_object_mode(obj):
    try:
        bpy.context.view_layer.objects.active = obj  # Set the object as the active object
        bpy.ops.object.mode_set(mode='OBJECT')
    except:
        pass

# ============== MODIFICATIONS ============== #
# In these functions we could check if the modifier with given name already exists, 
#  but we probably want to apply the same modifiers multiple times
def init_wireframe_modifier(obj, newThickness=0.1, newOffset=1):
    wireframe_modifier = obj.modifiers.new(name=WIREFRAME_MODIFIER_NAME, type='WIREFRAME')
    wireframe_modifier.thickness = newThickness # Thickness         # <0; 1>
    wireframe_modifier.offset = newOffset       # Offset            # <-1; 1>

def init_subdivision_modifier(obj, levels=1):
    if levels == 0:
        return
    subdivision_modifier = obj.modifiers.new(name=SUBDIVISION_MODIFIER_NAME, type='SUBSURF')
    subdivision_modifier.levels = levels        # Levels Viewport   # <0; 6>

def init_solidify_modifier(obj, newThickness=0.1, newOffset=1):
    solidify_modifier = obj.modifiers.new(name=SOLIDIFY_MODIFIER_NAME, type='SOLIDIFY')
    solidify_modifier.thickness = newThickness  # Thickness         # <-10; 10> (best to use <-0.5; 0.5>)
    solidify_modifier.offset = newOffset        # Offset            # <-1; 5>   (best to use >0)

def init_decimate_collapse_modifier(obj, newRatio=1):
    decimate_modifier = obj.modifiers.new(name=DECIMATE_MODIFIER_NAME, type='DECIMATE')
    decimate_modifier.decimate_type = 'COLLAPSE'
    decimate_modifier.ratio = newRatio         # Ratio   # <0; 1>

def init_decimate_planar_modifier(obj, newAngleLimit=1.0):
    decimate_modifier = obj.modifiers.new(name=DECIMATE_MODIFIER_NAME, type='DECIMATE')
    decimate_modifier.decimate_type = 'DISSOLVE'   # Planar
    #TYPE: float in [0, 3.14159], default 0.0872665
    decimate_modifier.angle_limit = newAngleLimit  # Ratio   # <0; 3.1459>

def enlarge(obj, distance):
    for vertex in obj.data.vertices:
        global_vertex_location = obj.matrix_world @ vertex.co
        direction = global_vertex_location - obj.location
        direction.normalize()
        new_vertex_location = global_vertex_location + distance * direction
        vertex.co = obj.matrix_world.inverted() @ new_vertex_location

def shrink(obj, distance):
    for vertex in obj.data.vertices:
        global_vertex_location = obj.matrix_world @ vertex.co
        direction = global_vertex_location - obj.location
        direction.normalize()
        new_vertex_location = global_vertex_location - distance * direction
        vertex.co = obj.matrix_world.inverted() @ new_vertex_location

def scale_object(obj, scale_factor):
    obj.scale = (scale_factor, scale_factor, scale_factor)

def stretch(obj, axis : str, stretch_factor : float):
    axis = axis.lower()
    if(axis == "x"):
        obj.scale.x *= stretch_factor
    elif(axis == "y"):
        obj.scale.y *= stretch_factor
    elif(axis == "z"):
        obj.scale.z *= stretch_factor
    else:
        return

# ============== FITNESS FUNCTIONS ============== #

# Calculates fitness for object's faces count
# - the less the faces = the bigger the fitness
def get_faces_count_fitness(obj, min_faces, max_faces):
    #remove_redundant_vertices(obj)
    
    # Get mesh data
    mesh = obj.data
    
    # Create bmesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Calculate faces
    faces_count = len(bm.faces)
    
    # If we exceed the max_faces with actual faces of the object, the fitness should be 0
    if faces_count > max_faces:
        return 0

    # Calculate the range of faces counts
    faces_range = max_faces - min_faces

    # Calculate the normalized value
    normalized_value = (faces_count - min_faces) / faces_range
    
    # Scale the normalized value to the fitness range
    fitness_value = (1 - normalized_value) * FITNESS_RANGE
    
    # Return fitness
    return fitness_value

# Calculates fitness for object's smoothness
def get_surface_smoothness_fitness(obj):
    # Calculate the average face angle of the object's mesh
    face_angles = []
    for face in obj.data.polygons:

        # Calculate the angle between adjacent face normals
        adjacent_normals = [obj.data.vertices[vert_index].normal for vert_index in face.vertices]
        angle_sum = 0
        for normal1, normal2 in zip(adjacent_normals, adjacent_normals[1:] + adjacent_normals[:1]):
            dot_product = np.dot(normal1, normal2)

            # Ensure that the dot product is within the valid range [-1, 1]
            dot_product = np.clip(dot_product, -1, 1)

            # Calculate the angle and add it to the sum
            angle_sum += np.arccos(dot_product)

        average_angle = angle_sum / len(face.vertices)
        face_angles.append(average_angle)
    
    # Filter out NaN values from face_angles
    valid_face_angles = [angle for angle in face_angles if not np.isnan(angle)]
    average_face_angle = np.mean(valid_face_angles)

    # Map the average face angle to the range [0, FITNESS_RANGE]
    fitness_value = FITNESS_RANGE - (np.degrees(average_face_angle) / 180) * FITNESS_RANGE
    return fitness_value

# Calculates fitness for object's bounding box volume fitness
def get_bounding_box_volume_fitness(obj, min_volume, max_volume):
    # Calculate the bounding box volume for the given object
    volume = get_bounding_box_volume(obj)

    if volume <= min_volume:
        return 0
    if volume >= max_volume:
        return 100
    
    # Normalize the volume to the range <0, 1>
    normalized_volume = (volume - min_volume) / (max_volume - min_volume)
    
    # Map the normalized volume to the fitness range
    fitness_value = normalized_volume * FITNESS_RANGE
    
    return fitness_value

# Gets the bounding box of an object and calculates its volume whilst taking into account the scaling
def get_bounding_box_volume(obj):
    # If the object is not a mesh, return 0
    if obj.type != 'MESH':
        return 0
    
    # Get the object's scale so it counts with it
    scale = obj.scale
    
    # Get the bounding box dimensions of the object
    bounding_box = obj.bound_box
    min_x = min(point[0] * scale[0] for point in bounding_box)
    max_x = max(point[0] * scale[0] for point in bounding_box)
    min_y = min(point[1] * scale[1] for point in bounding_box)
    max_y = max(point[1] * scale[1] for point in bounding_box)
    min_z = min(point[2] * scale[2] for point in bounding_box)
    max_z = max(point[2] * scale[2] for point in bounding_box)
    
    # Calculate the bounding box volume
    bounding_box_volume = (max_x - min_x) * (max_y - min_y) * (max_z - min_z)
    
    return bounding_box_volume

# Define the fitness function
def fitness_function(params):

    print("PARAMS: ", params)

    # Get the object
    object = get_all_objects_with_prefix(object_prefix)[0]

    # Set object mode
    set_object_mode(object)

    # Copy the object before changing it and hide its copy from viewport
    obj_copy = duplicate_object(object)
    obj_copy.hide_set(True)

    # Extract parameters
    decimate_modifier_offset = params[0]
    subdivision_modifier_levels = round(params[1] / 10)
    scale = params[2]

    # Initialize subdivision modifier (if subdivision_modifier_levels is zero, 
    init_subdivision_modifier(object, subdivision_modifier_levels)

    # Initialize decimate modifier
    init_decimate_collapse_modifier(object, decimate_modifier_offset)

    # Set new scale
    scale_object(object, scale)
    
    # apply all modifiers - in order to evaluate fitness, we need to have modifiers applied
    apply_all_modifiers(object)

    # Calculate fitness values
    smoothness_fitness = get_surface_smoothness_fitness(object)
    faces_count_fitness = get_faces_count_fitness(object, min_faces=20, max_faces=3000)
    bounding_box_volume_fitness = get_bounding_box_volume_fitness(object, 0.1, 50000)

    # Remove modified object and unhide its copy
    remove_object(object)
    obj_copy.hide_set(False)
    object = obj_copy

    # Return fitness values as a tuple
    return (faces_count_fitness, smoothness_fitness, bounding_box_volume_fitness)

def plotResults():
    # Extract objectives from algorithm results
    objectives = [solution.objectives for solution in algorithm.result]

    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract x, y, z values for each objective
    x_values = [obj[0] for obj in objectives]
    y_values = [obj[1] for obj in objectives]
    z_values = [obj[2] for obj in objectives]

    # Plot the Pareto front solutions
    ax.scatter(x_values, y_values, z_values, c='b', marker='o', label='Pareto Front Solutions')

    # Set labels for each axis
    ax.set_xlabel('Faces Count Fitness')
    ax.set_ylabel('Smoothness Fitness')
    ax.set_zlabel('BB Vol. Fitness')

    # Set title for the plot
    ax.set_title('Pareto Front Solutions')

    # Show the legend
    ax.legend()

    # Show the plot
    plt.show()

def get_best_and_worst_parameters(objectives, parameters, num_best=10, num_worst=10):
    # Combine objectives and parameters into tuples
    sorted_solutions = sorted(zip(objectives, parameters), key=lambda x: x[0][0], reverse=True)
    
    # Get the best parameters
    best_parameters = [solution[1] for solution in sorted_solutions[:num_best]]
    
    # Get the worst parameters
    worst_parameters = [solution[1] for solution in sorted_solutions[-num_worst:]]
    
    return best_parameters, worst_parameters

def apply_parameters_and_position_objects(best_parameters, worst_parameters, obj):
    # Create copies of the object for best and worst parameters
    best_objects = [obj.copy() for _ in range(len(best_parameters))]
    worst_objects = [obj.copy() for _ in range(len(worst_parameters))]
    
    # Link copies to the scene
    for best_obj in best_objects:
        bpy.context.collection.objects.link(best_obj)
    for worst_obj in worst_objects:
        bpy.context.collection.objects.link(worst_obj)
    
    # Apply parameters to copies for best and worst objects
    for best_obj, parameters in zip(best_objects, best_parameters):
        apply_parameters(best_obj, parameters)
    for worst_obj, parameters in zip(worst_objects, worst_parameters):
        apply_parameters(worst_obj, parameters)
    
    # Position copies in the scene
    middle_position = (len(best_objects) + 1) * 5 / 2  # Adjust spacing for the middle object
    for i, best_obj in enumerate(best_objects):
        best_obj.location.x += i * 5  # Adjust spacing between best objects
        best_obj.location.y += 5  # Adjust height of the row
        if i == len(best_objects) // 2:  # Place a gap for the middle object
            best_obj.location.x += 5
    
    for i, worst_obj in enumerate(worst_objects):
        worst_obj.location.x += i * 5 + middle_position  # Adjust spacing between worst objects
        worst_obj.location.y -= 5  # Adjust height of the row

def apply_parameters(obj, parameters):
    # Apply each parameter to the object according to their index
    for i, parameter in enumerate(parameters):
        if i == 0:
            init_decimate_collapse_modifier(obj, parameter)
        elif i == 1:
            init_subdivision_modifier(obj, parameter)
        elif i == 2:
            scale_object(obj, parameter)
        # Add more conditions as needed for additional parameters and modifiers

# ============== EXAMPLE USAGE ============== #

# Define prefix of the object we are working with so we can globally find it
object_prefix = "Cube"

# Define optimization problem
problem = Problem(3, 3)  # 3 parameters, 3 objectives

# first parameter is decimate ratio - more the ratio = more polygons, less ratio = less polygons
# second parameter is Catmull-Clark subdivision levels - more levels = smoother (and more polygons), less levels = more pointy (and less polygons)
# third time is scaling (in all directions) 
problem.types[:] = [Real(0.5, 1), Real(0, 30), Real(0.5, 2)]  # Parameter ranges
#problem.directions[:] = Problem.MAXIMIZE, Problem.MAXIMIZE, Problem.MAXIMIZE  # for all objectives
problem.function = fitness_function  # Fitness function

# Define and run the optimizer
algorithm = NSGAII(problem, population_size=100)
# This variator must be defined because of different types of problem.types 
algorithm.run(100)  # Number of generations

## Print the results
for solution in algorithm.result:
    solution.variables[1] = int(round(solution.variables[1]/10))
    print("Parameters:", solution.variables) # is a tuple containing the decision variable values (e.g., (size, decimation_ratio, print_speed)).
    print("Objectives:", solution.objectives) # is a tuple containing the fitness values evaluated by the fitness function (e.g., (weight, polygons, print_time)).

# Extract objective values and corresponding parameters from the algorithm results and round to 2 decimal places
objectives = [[round(val, 2) if isinstance(val, float) else val for val in solution.objectives] for solution in algorithm.result]
parameters = [[round(val, 2) if isinstance(val, float) else val for val in solution.variables] for solution in algorithm.result]

# Get our object
o = get_all_objects_with_prefix(object_prefix)[0]

# Get best and worst parameters
best_parameters, worst_parameters = get_best_and_worst_parameters(objectives, parameters)

# Call the function to apply parameters and position objects
apply_parameters_and_position_objects(best_parameters, worst_parameters, o)

# Plot results onto graph
plotResults()
