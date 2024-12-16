#### 특정 객체로 이동
import bpy

# 특정 객체 이름
object_name = "Plane"

# 객체가 존재하는지 확인
obj = bpy.data.objects.get(object_name)
if obj is None:
    print(f"Error: Object '{object_name}' not found.")
else:
    # 3D 뷰포트가 있는 영역을 찾기
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':  # 3D 뷰포트 영역 찾기
            for region in area.regions:
                if region.type == 'WINDOW':  # 윈도우 영역 찾기
                    space_data = area.spaces.active
                    space_data.region_3d.view_location = obj.location  # 객체 위치로 뷰포트 이동
                    print(f"Viewport moved to object location: {obj.location}")
                    break


# 객체가 존재하는지 확인
obj = bpy.data.objects.get(object_name)
if obj is None:
    print(f"Error: Object '{object_name}' not found.")
else:
    # 3D 뷰포트가 있는 영역을 찾기
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':  # 3D 뷰포트 영역 찾기
            for region in area.regions:
                if region.type == 'WINDOW':  # 윈도우 영역 찾기
                    space_data = area.spaces.active
                    space_data.region_3d.view_location = obj.location  # 객체 위치로 뷰포트 이동
                    print(f"Viewport moved to object location: {obj.location}")
                    break




