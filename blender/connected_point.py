#관 연결부분 표시


import bpy
import bmesh
import json
import math


state_geo = 'C:/Users/magpie/Desktop/pipePython/connection.json'
cen_str=json.load(open(state_geo, encoding='utf-8'))
coords_wgs84 = cen_str['coord']


# WGS84 좌표를 ECEF(3D 지구 중심 좌표)로 변환하는 함수
def wgs84_to_ecef(lat, lon):
    # WGS84 타원체 상수
    a = 6378137.0  # 장축 반지름 (meters)
    b = 6356752.314245  # 단축 반지름 (meters)
    e2 = 1 - (b * b) / (a * a)  # 이심률 제곱

    # 위도, 경도를 라디안으로 변환
    phi = math.radians(lat)
    lambda_ = math.radians(lon)

    # 반경 계산
    N = a / math.sqrt(1 - e2 * math.sin(phi) ** 2)

    # ECEF 좌표 계산
    X = (N + alt) * math.cos(phi) * math.cos(lambda_)
    Y = (N + alt) * math.cos(phi) * math.sin(lambda_)
    Z = ((b**2 / a**2) * N + alt) * math.sin(phi)

    return X, Y


# Blender 공간 내에서의 스케일링 팩터
scale_factor = 1 / 10  # 축소 비율 (ECEF 좌표가 너무 크므로 조정)

## 변환된 좌표를 저장할 배열
#ecef_coordinates = []

## 좌표 변환 및 저장
#for i in range(0,len(coords_wgs84)-1):
#    temp=[]
#    for lon, lat, alt in coords_wgs84[i]:  # 경도, 위도, 고도 순으로 언패킹
#        # WGS84 -> ECEF 변환
#        x, y, z = wgs84_to_ecef(lat, lon, alt)  # 위도, 경도를 올바르게 전달
#    
#        # 스케일링 적용
#        x, y, z = x * scale_factor, y * scale_factor, z * scale_factor
#    
#        # 배열에 추가
#        temp.append([x, y, z])
#    ecef_coordinates.append(temp)
## 결과 출력 (변환된 ECEF 좌표)


ecef_coordinates=[]
for i in range(0,len(coords_wgs84)-1):
    lon,lat,alt = coords_wgs84[i]
    x,y = wgs84_to_ecef(lat, lon)
    z=-alt*3
    x, y, z = x * scale_factor, y * scale_factor, z * scale_factor
    ecef_coordinates.append([x, y, z])
    
    
#for coord in ecef_coordinates:
#    bpy.ops.import_scene.gltf(filepath="C:\\Users\\magpie\\Desktop\\맨홀.glb", files=[{"name":"맨홀.glb", "name":"맨홀.glb"}], loglevel=20)
#    bpy.ops.object.join()

#    # 현재 활성 객체 가져오기
#    obj = bpy.context.view_layer.objects.active
#    # 객체 크기 줄이기
#    bpy.ops.transform.resize(
#        value=(0.5, 0.5, 0.5),  # 각 축에서 50%로 축소
#        orient_type='GLOBAL'
#    )
#    xPoint = 0
#    yPoint = 0
#    for c in coord:
#        xPoint = xPoint +c[0]
#        yPoint = yPoint +c[1]
#    xPoint = xPoint/len(coord)
#    yPoint = yPoint/len(coord)

#    # 특정 위치로 이동 (예: x=-0.83, y=-7.76, z=0.55)
#    obj.location = (xPoint+1,yPoint+1,2)
        
for coord in ecef_coordinates:
#    bpy.ops.import_scene.gltf(filepath="C:\\Users\\magpie\\Desktop\\맨홀.glb", files=[{"name":"맨홀.glb", "name":"맨홀.glb"}], loglevel=20)
#    bpy.ops.object.join()

#    # 현재 활성 객체 가져오기
#    obj = bpy.context.view_layer.objects.active
#    # 객체 크기 줄이기
#    bpy.ops.transform.resize(
#        value=(0.2, 0.2, 0.2),  # 각 축에서 50%로 축소
#        orient_type='GLOBAL'
#    )
#    obj.location = (coord[0]+1,coord[1]+1,coord[2])
    bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(coord[0]+1,coord[1]+1,coord[2]), scale=(0.25, 0.25, 0.25))