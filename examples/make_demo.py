# SPDX-License-Identifier: GPL-3.0-or-later
"""Blender factory-startup fixture and complete hashed public lighting request.

Run: blender --background --factory-startup --disable-autoexec --offline-mode
--python-exit-code 23 --python examples/make_demo.py -- /absolute/demo-directory
"""
import sys,json,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
dest=Path(sys.argv[sys.argv.index('--')+1]).resolve();dest.mkdir(parents=True,exist_ok=True)
source=dest/'demo-source.blend'
if source.exists():raise RuntimeError('Refusing to overwrite an existing demo source')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,location=(0,0,1));obj=bpy.context.object;obj.name='DemoProduct'
for p in obj.data.polygons:p.use_smooth=True
m=bpy.data.materials.new('DemoMetal');m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(.4,.23,.08,1);n.inputs['Metallic'].default_value=.7;n.inputs['Roughness'].default_value=.3;obj.data.materials.append(m)
bpy.ops.mesh.primitive_plane_add(size=12);bpy.context.object.name='DemoFloor'
camd=bpy.data.cameras.new('DemoCamera.Data');cam=bpy.data.objects.new('DemoCamera',camd);bpy.context.scene.collection.objects.link(cam)
cam.location=(4,-6,3);cam.rotation_euler=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.scene.camera=cam
bpy.ops.wm.save_as_mainfile(filepath=str(source),check_existing=False)
manifest={'version':'1.0','scene':bpy.context.scene.name,'view_layer':bpy.context.view_layer.name,'rig_id':'demo','action':'create','targets':[obj.name],'mode':'relight','anchor':'world',
 'lights':[{'id':'key','role':'key','type':'AREA','location':[-1,-2,2],'energy':300,'color':[1,.9,.8],'size':2},{'id':'fill','role':'fill','type':'AREA','location':[1,-1,1],'energy':90,'color':[.75,.85,1],'size':2}],
 'boards':[{'id':'flag','kind':'flag','location':[1,0,1],'rotation_deg':[0,60,0],'size':[.4,1],'enabled':False}],
 'world':{'kind':'constant','color':[.04,.04,.04],'strength':.2},'eevee':{'use_raytracing':True}}
request={'schema_version':'1.0','command':'lighting.run','params':{'file':str(source),'expected_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'resources':[],'manifest':manifest,
 'preview':{'engines':['CYCLES','BLENDER_EEVEE'],'device':{'backend':'CPU'},'width':128,'height':128,'samples':16,'denoise':True}}}
(dest/'request.json').write_text(json.dumps(request,indent=2),encoding='utf-8');print('Demo ready:',dest/'request.json')
