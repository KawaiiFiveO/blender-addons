bl_info = {
    "name": "Material Cleanup Tool",
    "author": "OneHalf",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "3D View > Object > Material Cleanup",
    "description": "Automatically replace materials with suffixes like '.001' with their base counterparts",
    "category": "Material",
}

import bpy
import re

def clean_up_materials(context):
    # Get all materials in the file
    material_dict = {mat.name: mat for mat in bpy.data.materials}

    # Iterate over all objects in the scene
    for obj in bpy.data.objects:
        if obj.type == 'MESH':  # Only process mesh objects
            for slot in obj.material_slots:
                mat_name = slot.material.name if slot.material else None
                if mat_name:
                    # Use regex to strip numerical suffixes (e.g., ".001")
                    base_name = re.sub(r"\.\d{3}$", "", mat_name)
                    if base_name in material_dict and base_name != mat_name:
                        slot.material = material_dict[base_name]
                        print(f"Replaced {mat_name} with {base_name} on {obj.name}")

class MATERIAL_OT_cleanup(bpy.types.Operator):
    """Replace materials with suffixes like '.001' with their base counterparts"""
    bl_idname = "material.cleanup"
    bl_label = "Clean Up Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        clean_up_materials(context)
        self.report({'INFO'}, "Material cleanup completed!")
        return {'FINISHED'}

class MATERIAL_PT_cleanup_panel(bpy.types.Panel):
    """Creates a panel in the 3D view"""
    bl_label = "Material Cleanup Tool"
    bl_idname = "MATERIAL_PT_cleanup_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Material Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator(MATERIAL_OT_cleanup.bl_idname)

def register():
    bpy.utils.register_class(MATERIAL_OT_cleanup)
    bpy.utils.register_class(MATERIAL_PT_cleanup_panel)

def unregister():
    bpy.utils.unregister_class(MATERIAL_OT_cleanup)
    bpy.utils.unregister_class(MATERIAL_PT_cleanup_panel)

if __name__ == "__main__":
    register()
