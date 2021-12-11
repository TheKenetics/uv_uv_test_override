bl_info = {
	"name": "UVTest Override",
	"author": "Kenetics",
	"version": (0, 1),
	"blender": (3, 0, 0),
	"location": "View3D > Operator Search > Toggle UVTest Override",
	"description": "Toggles material override for UVTest material.",
	"warning": "",
	"wiki_url": "",
	"category": "UV"
}

import bpy
from bpy.props import EnumProperty, IntProperty, FloatVectorProperty, BoolProperty, FloatProperty, StringProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, AddonPreferences


## Constants
# Set to true when debugging, enables debug print statements and stuff
DEBUGGING = False


## Helper Functions
def get_addon_preferences():
	return bpy.context.preferences.addons[__package__].preferences

def dprint(print_string):
	# print debug string
	if DEBUGGING:
		print(f"[DEBUG] {__package__}: {print_string}")


## Operators
class UVTO_OT_toggle_uv_test_override(Operator):
	"""Toggle UVTest override material."""
	bl_idname = "uvto.toggle_uv_test_override"
	bl_label = "Toggle UVTest Material"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		prefs = get_addon_preferences()
		uvtest_mat_name = prefs.uv_test_mat_name
		uvtest_mat = bpy.data.materials.get(uvtest_mat_name, None)
		
		## Error Checking
		if uvtest_mat is None:
			self.report({"ERROR"}, "No UVTest material found.")
			return {'CANCELLED'}
		
		## Toggle
		if context.view_layer.material_override is not uvtest_mat:
			dprint(f"Material override ({context.view_layer.material_override}) is not UVTest ({uvtest_mat})")
			dprint("Switching to UVTest mat")
			context.scene.uvto_old_override_material = context.view_layer.material_override
			dprint(f"Cached old material ({context.scene.uvto_old_override_material})")
			context.view_layer.material_override = uvtest_mat
		else:
			dprint(f"Material override ({context.view_layer.material_override}) is UVTest ({uvtest_mat})")
			dprint(f"Switching to old material ({context.scene.uvto_old_override_material})")
			context.view_layer.material_override = context.scene.uvto_old_override_material
		
		dprint("Switched!")
		
		return {'FINISHED'}


## Preferences
class UVTO_addon_preferences(AddonPreferences):
	bl_idname = __package__
	
	# Properties
	show_mini_manual : BoolProperty(name="Show Mini Manual", default=False)

	uv_test_mat_name : StringProperty(
		name="UVTest Material Name",
		description="Name of UVTest material to switch to.",
		default="UVTest"
	)

	def draw(self, context):
		layout = self.layout
		
		layout.prop(self, "uv_test_mat_name")
		
		# Mini manual
		layout.prop(self, "show_mini_manual", toggle=True)
		if self.show_mini_manual:
			layout.label(text="Using", icon="DOT")
			layout.label(text="This addon allows you to easily toggle a UVTest override material on/off.",icon="THREE_DOTS")
			layout.label(text="Just set the UVTest Material Name to whatever your UV testing material is.",icon="THREE_DOTS")
			layout.label(text="Then in the 3D View, open Operator Search, and run Toggle UVTest Material",icon="THREE_DOTS")


## Register
classes = (
	UVTO_OT_toggle_uv_test_override,
	UVTO_addon_preferences
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
	## Add Custom Properties
	bpy.types.Scene.uvto_old_override_material = PointerProperty(type=bpy.types.Material)

def unregister():
	## Remove Custom Properties
	del bpy.types.Scene.uvto_old_override_material
	
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()
