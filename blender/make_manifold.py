import bpy

def main(input_file, output_file):
    # Delete everything in the scene.
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

    # Import the model, scale down, and rotate 90 deg about x.
    bpy.ops.import_mesh.stl(filepath=input_file)
    bpy.ops.transform.resize(value=(0.01, 0.01, 0.01), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)  # apply all transforms

    # Merge vertices by distance.
    bpy.ops.object.editmode_toggle()  # edit mode
    bpy.ops.mesh.select_all(action='SELECT')  # select all vertices
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()

    # Add solidify modifier.
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = 0.05
    bpy.ops.object.modifier_apply(modifier="Solidify")

    # Export mesh.
    bpy.ops.export_mesh.stl(filepath=out_file)

if __name__ == "__main__":
    test_file = "M:\\3d_printing\\star_citizen\\downloads\\400i_400i.stl"
    out_file = "M:\\3d_printing\\star_citizen\\edited\\400i_400i.stl"
    main(test_file, out_file)