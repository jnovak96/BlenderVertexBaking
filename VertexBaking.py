import bpy
import bmesh

lightmap_w = 1024
lightmap_h = 1024
env_samples = 12
margin = 4


D = bpy.data
o = bpy.context.selected_objects[0]
m = bpy.data.materials[o.active_material.name]

# generate lightmap image
if "lightmap_img" not in bpy.data.images:    
    image = bpy.data.images.new("lightmap_img", width=lightmap_w, height=lightmap_h)
else:
    bpy.data.images.remove(bpy.data.images["lightmap_img"])
    image = bpy.data.images.new("lightmap_img", width=lightmap_w, height=lightmap_h)

# add uv lightmap
uv_lm = o.data.uv_layers.get("UV_lightmap")
if not uv_lm:
    uv_lm = o.data.uv_layers.new(name="UV_lightmap")
uv_lm.active = True
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT') # for all faces
bpy.ops.uv.lightmap_pack(PREF_CONTEXT='SEL_FACES', PREF_PACK_IN_ONE=True, PREF_NEW_UVLAYER=False, PREF_BOX_DIV=12, PREF_MARGIN_DIV=0.1)

#add nodes to materials
img_node = m.node_tree.nodes.new("ShaderNodeTexImage")
uv_node = m.node_tree.nodes.new("ShaderNodeUVMap")
m.node_tree.links.new(uv_node.outputs["UV"], img_node.inputs["Vector"])
img_node.image = image
uv_node.uv_map = "UV_lightmap"

#bake lightmap
D.scenes["Scene"].cycles.samples = env_samples
D.scenes["Scene"].cycles.bake_type = 'DIFFUSE'
D.scenes["Scene"].render.bake.use_pass_direct = True
D.scenes["Scene"].render.bake.use_pass_indirect = True
D.scenes["Scene"].render.bake.use_pass_color = False
D.scenes["Scene"].render.bake.margin = margin
D.scenes["Scene"].render.bake.use_clear = False
D.scenes["Scene"].display_settings.display_device = 'sRGB'
bpy.ops.object.bake(type = 'DIFFUSE')
