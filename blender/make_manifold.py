import bpy

def print_toolbox_make_manifold():
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=True)
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_interior_faces()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.dissolve_degenerate(threshold=0.0001)
    bpy.ops.mesh.select_non_manifold(extend=False, use_wire=True, use_boundary=True, use_multi_face=False, use_non_contiguous=False, use_verts=True)
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent()
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.print3d_clean_non_manifold()


def main(input_file, output_file):
    # Delete everything in the scene.
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

    # Import the model, scale down, and rotate 90 deg about x.
    print(f"Importing: {input_file}")
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
    print("Solidify Modifier")
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = 0.05
    bpy.ops.object.modifier_apply(modifier="Solidify")

    # Do the subdivision surface modifier.
    print("Subdivision Surface Modifier")
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 1  # Levels of subdivision.
    bpy.ops.object.modifier_apply(modifier="Subdivision")

    # Apply Remesh Modifier.
    print("Remesh Modifier")
    bpy.ops.object.modifier_add(type='REMESH')
    bpy.context.object.modifiers["Remesh"].voxel_size = 0.01  # Size of voxels in meters.
    bpy.ops.object.modifier_apply(modifier="Remesh")

    # Decimate the mesh where there is lots of flat geometry.
    print("Decimate Modifier")
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].ratio = 0.1
    bpy.ops.object.modifier_apply(modifier="Decimate")

    # Run the 3D Print toolbox's "Make Manifold" button.
    print("3D-Print Toolbox Make Manifold")
    print_toolbox_make_manifold()

    # Export mesh.
    print(f"Exporting: {out_file}")
    bpy.ops.export_mesh.stl(filepath=out_file)

if __name__ == "__main__":
    test_file = "M:\\3d_printing\\star_citizen\\downloads\\drake-cutlass_Cutlass-Black.stl"
    out_file = "M:\\3d_printing\\star_citizen\\edited\\drake-cutlass_Cutlass-Black.stl"
    main(test_file, out_file)