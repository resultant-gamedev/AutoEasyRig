import bpy
from bpy.app.handlers import persistent

rigBoneDico = {} 
pickerBoneDico ={}

if bpy.context.object:
    if  bpy.context.object.type == 'ARMATURE':
        if  bpy.context.object.mode == 'POSE':
            if bpy.context.object.name.endswith('_picker') :
                
                picker = bpy.context.object
                rig = bpy.data.objects.get(bpy.context.object.name.replace('_picker',''))
                
            else :
                rig = bpy.context.object
                picker = bpy.data.objects.get(rig.name+'_picker')
            
            #for bone in bpy.context.visible_pose_bones:
            if picker :                 
                for pickerBone in picker.pose.bones:
                    bone = rig.pose.bones.get(pickerBone.name)
                    pBone = pickerBone
                    ppBone= pickerBone
                    
                    if bone :
                        rigBoneDico[bone.name]=bone.bone.select
                        pickerBoneDico[bone.name]=ppBone.bone.select

def proxyPickerSelectDef():
    if bpy.context.object:
        if  bpy.context.object.type == 'ARMATURE':
            if  bpy.context.object.mode == 'POSE':
                if bpy.context.object.name.endswith('_picker') :
                    
                    picker = bpy.context.object
                    rig = bpy.data.objects.get(bpy.context.object.name.replace('_picker',''))
                    
                else :
                    rig = bpy.context.object
                    picker = bpy.data.objects.get(rig.name+'_picker')
                
                #for bone in bpy.context.visible_pose_bones:
                if picker :                 
                    for pickerBone in picker.pose.bones:
                        #print(rigBoneDico)
                        #print(pickerBoneDico)
                        bone = rig.pose.bones.get(pickerBone.name)
                        pBone = pickerBone
                        ppBone= pickerBone
                        
                        if ppBone:    
                            if not ppBone.name.endswith('.operator'):
                                if bone :
                                    if bone.bone.select != rigBoneDico[bone.name]:
                                        ppBone.bone.select = bone.bone.select
                                        rigBoneDico[bone.name]=bone.bone.select
                                        #bpy.context.scene.objects.active = rig
                                      

                                    if ppBone.bone.select != pickerBoneDico[ppBone.name]:
                                        #ppBone.bone.select = False
                                        bone.bone.select =  ppBone.bone.select
                                        pickerBoneDico[ppBone.name]=ppBone.bone.select


                                    for modifier in ppBone.custom_shape.modifiers :
                                        if modifier.type == 'UV_WARP':
                                            if ppBone.bone.select :
                                                modifier.center[1] = 0.01                                   
                                            else :
                                                modifier.center[1] = ppBone['color_orig']
                                        
                        if bpy.context.object == picker:
                            bpy.context.scene.objects.active = rig
                            picker.select =False                                       
                                #selectProxyPickerBone(rig,ppBone,Select=True)
@persistent
def proxyPickerSelect(dummy):
    proxyPickerSelectDef()

def register():
    bpy.app.handlers.scene_update_pre.append(proxyPickerSelect)
def unregister():
                           

    bpy.app.handlers.scene_update_pre.remove(proxyPickerSelect)
    
register()
#unregister()