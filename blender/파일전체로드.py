import bpy
import bmesh
import sys
import json
import os

#파일 정보 로드
def fileList(dir_path):
    folder_dir = dir_path
    fileNameList =os.listdir(folder_dir)
    return fileNameList

#geojson list
fileName_list = fileList('C:/Users/magpie/Desktop/pipe프로젝트관련/PipeData_Create/data')

for file in fileName_list:
    
    #속성정보가 포함된 데이터(z값, 관경)
    #state_geo = 'C:/Users/magpie/Desktop/pipePython/유수관데이터.json'
    state_geo = "C:/Users/magpie/Desktop/pipe프로젝트관련/PipeData_Create/data/{0}".format(file)
    #state_geo = 'C:/Users/magpie/Desktop/pipePython/오수관데이터.json'
    cen_str=json.load(open(state_geo, encoding='utf-8'))
    for data in cen_str:
        
        coords_wgs84 = data['coord']


        import math

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

        # 변환된 좌표를 저장할 배열
        ecef_coordinates = []

        # 좌표 변환 및 저장
        for i in range(0,len(coords_wgs84)-1):
            temp=[]
            for lon, lat, alt in coords_wgs84[i]:  # 경도, 위도, 고도 순으로 언패킹
                # WGS84 -> ECEF 변환
                x, y= wgs84_to_ecef(lat, lon)  # 위도, 경도를 올바르게 전달
                z = -alt*3
                # 스케일링 적용
                x, y, z = x * scale_factor, y * scale_factor, z * scale_factor
            
                # 배열에 추가
                temp.append([x, y, z])
            ecef_coordinates.append(temp)
        # 결과 출력 (변환된 ECEF 좌표)
        print(ecef_coordinates)





        def createVector(X,Y,Z):
            bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(X,Y,Z), scale=(1, 1, 1))
            bpy.ops.object.editmode_toggle()
            #bpy.ops.mesh.delete(type='VERT')
            obj = bpy.context.object
            if obj is not None and obj.type == 'MESH':
                # BMesh를 사용하여 메쉬 편집 모드로 작업
                bm = bmesh.from_edit_mesh(obj.data)
            
                # 삭제하려는 꼭지점 인덱스를 리스트로 정의 (예: 0, 1, 2번 꼭지점)
                vertices_to_delete = [0, 1, 2]
            
                # 꼭지점을 선택
                for v in bm.verts:
                    if v.index in vertices_to_delete:
                        v.select = True
                    else:
                        v.select = False  # 다른 꼭지점은 선택 해제

                # 선택된 꼭지점 삭제
                bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.select], context='VERTS')
            
            
                for v in bm.verts:
                    if v.index in vertices_to_delete:
                        v.select = True


                    
            
        def extrude_and_move(value=(0, 0, 1), constraint_axis=(False, False, True), orient_type='GLOBAL'):
            """
            Extrude 선택된 영역을 주어진 방향으로 이동.

            Parameters:
            - value (tuple): 이동 거리 (X, Y, Z 축으로 설정 가능).
            - orient_type (str): 좌표계 유형 ('GLOBAL', 'LOCAL', etc.).
            - constraint_axis (tuple): 이동 제약 방향 (X, Y, Z를 각각 True/False로 설정).
            """
            bpy.ops.mesh.extrude_region_move(
                MESH_OT_extrude_region={
                    "use_normal_flip": False,
                    "use_dissolve_ortho_edges": False,
                    "mirror": False
                },
                TRANSFORM_OT_translate={
                    "value": value,
                    "orient_type": orient_type,
                    "constraint_axis": constraint_axis,
                    "use_proportional_edit": False
                }
            )




        for i in range(len(ecef_coordinates)):
            ecef_coordinates_ = ecef_coordinates[i]
            createVector(ecef_coordinates_[0][0],ecef_coordinates_[0][1],ecef_coordinates_[0][2])
            previous_coord = ecef_coordinates_[0]
            for coord in ecef_coordinates_[1:]:
               delta = [c - p for c, p in zip(coord, previous_coord)]
               extrude_and_move(value=delta, constraint_axis=(True, True, False))
               previous_coord = coord


            bpy.ops.object.editmode_toggle()
            bpy.ops.object.convert(target='CURVE')
            bpy.context.object.data.bevel_depth = 0.15
            bpy.context.object.data.bevel_resolution = 14
        #    bpy.context.object.data.use_fill_caps = True
            bpy.ops.object.shade_smooth()
            bpy.ops.object.convert(target='MESH')
             # 재질 생성 및 색상 지정
            obj = bpy.context.object  # 현재 활성화된 객체
            mat = bpy.data.materials.new(name=f"Material_{i}")  # 새로운 재질 생성
            mat.use_nodes = True  # 노드 기반 재질 활성화

            # 노드에 색상 추가
            bsdf = mat.node_tree.nodes.get('Principled BSDF')  # 기본 BSDF 노드 가져오기
            if bsdf:  # BSDF 노드가 있는지 확인
                bsdf.inputs['Base Color'].default_value = (0.0, 1.0, 0.0, 1.0)  # 빨간색 RGBA 값 (0~1)

            # 객체에 재질 적용
            if obj.data.materials:
                obj.data.materials[0] = mat  # 기존 재질을 덮어씀
            else:
                obj.data.materials.append(mat)  # 새로운 재질 추가
            
        #bpy.ops.material.new()
        #bpy.context.object.active_material.name = "Material.005"
        #bpy.data.materials["Material.005"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.00343534, 0.00218607, 0.800047, 1)
