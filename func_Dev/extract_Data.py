# import ezdxf
# import geojson
# from shapely.geometry import mapping, Polygon, Point, LineString

# # DWF 파일 읽기
# def extract_layer_to_geojson(dwf_file, layer_name, output_geojson):
#     # DWF 파일 열기
#     try:
#         dwg = ezdxf.readfile(dwf_file)
#     except Exception as e:
#         print(f"Error reading DWF file: {e}")
#         return
    
#     # GeoJSON Feature 리스트 초기화
#     features = []

#     # 해당 레이어의 엔티티 추출
#     modelspace = dwg.modelspace()
#     for entity in modelspace:
#         if entity.dxf.layer == layer_name:
#             # 엔티티 타입 확인
#             if entity.dxftype() == 'LINE':
#                 geometry = LineString([(entity.dxf.start.x, entity.dxf.start.y),
#                                        (entity.dxf.end.x, entity.dxf.end.y)])
#             elif entity.dxftype() == 'CIRCLE':
#                 geometry = Point(entity.dxf.center.x, entity.dxf.center.y).buffer(entity.dxf.radius)
#             elif entity.dxftype() == 'LWPOLYLINE':
#                 points = [(point[0], point[1]) for point in entity.get_points()]
#                 geometry = Polygon(points) if len(points) > 2 else LineString(points)
#             else:
#                 print(f"Unsupported entity type: {entity.dxftype()}")
#                 continue
            
#             # GeoJSON Feature 추가
#             features.append(geojson.Feature(geometry=mapping(geometry), properties={"layer": layer_name}))

#     # GeoJSON 파일 저장
#     with open(output_geojson, 'w') as f:
#         geojson.dump(geojson.FeatureCollection(features), f, indent=2)
#     print(f"GeoJSON saved to {output_geojson}")

# # 사용법
# dwf_file_path = "C:/cadFile/convert/377090200.dxf"
# target_layer = "제원"
# output_geojson_path = "C:/cadFile/convert/result.geojson"

# extract_layer_to_geojson(dwf_file_path, target_layer, output_geojson_path)



'''TEXT 속성값까지 추출'''
# import ezdxf
# import geojson
# from shapely.geometry import mapping, Polygon, Point, LineString

# # DWF 파일 읽기
# def extract_layer_to_geojson(dwf_file, layer_name, output_geojson):
#     # DWF 파일 열기
#     try:
#         dwg = ezdxf.readfile(dwf_file)
#     except Exception as e:
#         print(f"Error reading DWF file: {e}")
#         return
    
#     # GeoJSON Feature 리스트 초기화
#     features = []

#     # 해당 레이어의 엔티티 추출
#     modelspace = dwg.modelspace()
#     for entity in modelspace:
#         if entity.dxf.layer == layer_name:
#             # 엔티티 타입 확인
#             if entity.dxftype() == 'LINE':
#                 geometry = LineString([(entity.dxf.start.x, entity.dxf.start.y),
#                                        (entity.dxf.end.x, entity.dxf.end.y)])
#                 properties = {"type": "LINE", "layer": layer_name}
#             elif entity.dxftype() == 'CIRCLE':
#                 geometry = Point(entity.dxf.center.x, entity.dxf.center.y).buffer(entity.dxf.radius)
#                 properties = {"type": "CIRCLE", "layer": layer_name, "radius": entity.dxf.radius}
#             elif entity.dxftype() == 'LWPOLYLINE':
#                 points = [(float(point[0]), float(point[1])) for point in entity.get_points()]
#                 geometry = LineString(points)
#                 properties = {"type": "LWPOLYLINE", "layer": layer_name}
#             elif entity.dxftype() == 'TEXT':
#                 geometry = Point(entity.dxf.insert.x, entity.dxf.insert.y)
#                 properties = {
#                     "type": "TEXT",
#                     "layer": layer_name,
#                     "text": entity.dxf.text,
#                     "height": entity.dxf.height,
#                 }
#             else:
#                 print(f"Unsupported entity type: {entity.dxftype()}")
#                 continue
            
#             # GeoJSON Feature 추가
#             features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

#     # GeoJSON 파일 저장
#     with open(output_geojson, 'w') as f:
#         geojson.dump(geojson.FeatureCollection(features), f, indent=2)
#     print(f"GeoJSON saved to {output_geojson}")


# #추출해야할 정보
# layerList =['SBA001','SBA002','SBA003','SBA004','SBA900','SBA999', #관 정보
#                  'SBD001','SBD002','SBD003','SBD004',                   #맨 홀
#                  'SB101','SB102',                                       #물받이
#                  '제원','하수제원']                                      #제원


# # 사용법
# dwf_file_path = "C:/cadFile/convert/377090300.dxf"
# target_layer = "하수제원"
# output_geojson_path = "C:/cadFile/convert/377090300_하수제원.geojson"

# extract_layer_to_geojson(dwf_file_path, target_layer, output_geojson_path)


'''ID 값 추가'''


# import ezdxf
# import geojson
# import uuid
# from shapely.geometry import mapping, Polygon, Point, LineString

# # DWF 파일 읽기
# def extract_layer_to_geojson_with_ids(dwf_file, layer_name, output_geojson):
#     # DWF 파일 열기
#     try:
#         dwg = ezdxf.readfile(dwf_file)
#     except Exception as e:
#         print(f"Error reading DWF file: {e}")
#         return
    
#     # GeoJSON Feature 리스트 초기화
#     features = []

#     # 해당 레이어의 엔티티 추출
#     modelspace = dwg.modelspace()
#     for idx, entity in enumerate(modelspace):
#         if entity.dxf.layer == layer_name:
#             # 엔티티 타입 확인
#             if entity.dxftype() == 'LINE':
#                 geometry = LineString([(entity.dxf.start.x, entity.dxf.start.y),
#                                        (entity.dxf.end.x, entity.dxf.end.y)])
#                 properties = {"type": "LINE", "layer": layer_name}
                
#             elif entity.dxftype() == 'CIRCLE':
#                 geometry = Point(entity.dxf.center.x, entity.dxf.center.y).buffer(entity.dxf.radius)
#                 properties = {"type": "CIRCLE", "layer": layer_name, "radius": entity.dxf.radius}

#             elif entity.dxftype() == 'LWPOLYLINE':
#                 points = [(point[0], point[1]) for point in entity.get_points()]
#                 # geometry = Polygon(points) if len(points) > 2 else LineString(points)
#                 geometry = LineString(points)
#                 properties = {"type": "LWPOLYLINE", "layer": layer_name}

#             elif entity.dxftype() == 'TEXT':
#                 geometry = Point(entity.dxf.insert.x, entity.dxf.insert.y)
#                 properties = {
#                     "type": "TEXT",
#                     "layer": layer_name,
#                     "text": entity.dxf.text,
#                     "height": entity.dxf.height,
#                 }
#             else:
#                 print(f"Unsupported entity type: {entity.dxftype()}")
#                 continue
            
#             # 고유 ID 추가
#             # properties["id"] = "{0}_{1}".format(idx,str(uuid.uuid4()))

#             # GeoJSON Feature 추가
#             features.append({"{0}_{1}".format(idx,str(uuid.uuid4())):geojson.Feature(geometry=mapping(geometry), properties=properties)})
            

#     # GeoJSON 파일 저장
#     with open(output_geojson, 'w') as f:
#         geojson.dump(geojson.FeatureCollection(features), f, indent=2)
#     print(f"GeoJSON saved to {output_geojson}")

# # 사용법
# dwf_file_path = "C:/cadFile/convert/377090200.dxf"
# target_layer = "SBA003"
# output_geojson_path = "C:/cadFile/convert/SBA003.geojson"

# extract_layer_to_geojson_with_ids(dwf_file_path, target_layer, output_geojson_path)



'''dxf 파일 layer 추출'''

# import ezdxf
# import geojson
# from shapely.geometry import mapping, Point, LineString

# def extract_all_layers_to_geojson(dwf_file, layer_list, output_geojson_path):
#     """
#     모든 레이어 데이터를 GeoJSON으로 추출, 한글 레이어 이름 처리 포함.
    
#     :param dwf_file: DWF 파일 경로
#     :param layer_list: 처리할 레이어 ID 리스트
#     :param output_geojson_path: GeoJSON 파일 저장 경로
#     """
#     try:
#         dwg = ezdxf.readfile(dwf_file)
#     except Exception as e:
#         print(f"Error reading DWF file: {e}")
#         return

#     # GeoJSON 데이터를 저장할 딕셔너리
#     layer_data = {}

#     # 각 레이어 처리
#     modelspace = dwg.modelspace()
#     for layer_name in layer_list:
#         features = []  # 해당 레이어의 GeoJSON Feature 저장
#         for entity in modelspace:
#             print(entity.dxf.layer)
#             if entity.dxf.layer == layer_name:
#                 # 엔티티 처리
#                 if entity.dxftype() == 'LINE':
#                     geometry = LineString([(entity.dxf.start.x, entity.dxf.start.y),
#                                            (entity.dxf.end.x, entity.dxf.end.y)])
#                     properties = {"type": "LINE", "layer": layer_name}

#                 elif entity.dxftype() == 'CIRCLE':
#                     geometry = Point(entity.dxf.center.x, entity.dxf.center.y).buffer(entity.dxf.radius)
#                     properties = {"type": "CIRCLE", "layer": layer_name, "radius": entity.dxf.radius}

#                 elif entity.dxftype() == 'LWPOLYLINE':
#                     points = [(point[0], point[1]) for point in entity.get_points()]
#                     # geometry = Polygon(points) if len(points) > 2 else LineString(points)
#                     geometry = LineString(points)
#                     properties = {"type": "LWPOLYLINE", "layer": layer_name}

#                 elif entity.dxftype() == 'TEXT':
#                     geometry = Point(entity.dxf.insert.x, entity.dxf.insert.y)
#                     properties = {
#                         "type": "TEXT",
#                         "layer": layer_name,
#                         "text": entity.dxf.text,
#                         "height": entity.dxf.height,
#                     }
#                 else:
#                     print(f"Unsupported entity type: {entity.dxftype()}")
#                     continue

#                 # GeoJSON Feature 추가
#                 features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

#         # 레이어 저장
#         layer_data[layer_name] = geojson.FeatureCollection(features)
#         print(f"Layer {layer_name} processed with {len(features)} features.")

#     # GeoJSON 저장 (ensure_ascii=False로 한글 처리)
#     with open(output_geojson_path, 'w', encoding='utf-8') as f:
#         geojson.dump(layer_data, f, indent=2, ensure_ascii=False)
#     print(f"GeoJSON saved to {output_geojson_path}")


# # 레이어 리스트와 파일 경로
# layer_list = [
#     'SBD001'
# ]
# # layer_list = [
# #     'SBA001', 'SBA002', 'SBA003', 'SBA004', 'SBA900', 'SBA999','SBD001', 'SBD002', 'SBD003', 'SBD004','SB101', 'SB102','제원', '하수제원'
# # ]
# dwf_file_path = "C:/cadFile/convert/377090300.dxf"
# output_geojson_path = "C:/cadFile/convert/377090300_all_layers_fixed.geojson"

# # 실행
# extract_all_layers_to_geojson(dwf_file_path, layer_list, output_geojson_path)



'''INSET TYPE 추가'''

# import ezdxf
# import geojson
# from shapely.geometry import mapping, Point, LineString

# def extract_all_layers_to_geojson(dwf_file, layer_list, output_geojson_path):
#     try:
#         dwg = ezdxf.readfile(dwf_file)
#     except Exception as e:
#         print(f"Error reading DWF file: {e}")
#         return

#     layer_data = {}
#     modelspace = dwg.modelspace()

#     for layer_name in layer_list:
#         features = []
#         for entity in modelspace:
#             if entity.dxf.layer == layer_name:
#                 if entity.dxftype() == 'LINE':
#                     geometry = LineString([(entity.dxf.start.x, entity.dxf.start.y),
#                                            (entity.dxf.end.x, entity.dxf.end.y)])
#                     properties = {"type": "LINE", "layer": layer_name}
#                     features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

#                 elif entity.dxftype() == 'TEXT':
#                     geometry = Point(entity.dxf.insert.x, entity.dxf.insert.y)
#                     properties = {
#                         "type": "TEXT",
#                         "layer": layer_name,
#                         "text": entity.dxf.text,
#                         "height": entity.dxf.height,
#                     }
#                     features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

#                 elif entity.dxftype() == 'INSERT':
#                     block_name = entity.dxf.name
#                     print(f"INSERT entity in layer {layer_name}, Block: {block_name}")
#                     block = dwg.blocks.get(block_name)
#                     for sub_entity in block:
#                         if sub_entity.dxftype() == 'LINE':
#                             geometry = LineString([(sub_entity.dxf.start.x, sub_entity.dxf.start.y),
#                                                    (sub_entity.dxf.end.x, sub_entity.dxf.end.y)])
#                             properties = {"type": "LINE", "layer": layer_name, "block": block_name}
#                             features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))
#                         elif sub_entity.dxftype() == 'TEXT':
#                             geometry = Point(sub_entity.dxf.insert.x, sub_entity.dxf.insert.y)
#                             properties = {
#                                 "type": "TEXT",
#                                 "layer": layer_name,
#                                 "block": block_name,
#                                 "text": sub_entity.dxf.text,
#                                 "height": sub_entity.dxf.height,
#                             }
#                             features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))
#                         else:
#                             print(f"Unsupported sub-entity type in block {block_name}: {sub_entity.dxftype()}")

#                 else:
#                     print(f"Unsupported entity type in layer {layer_name}: {entity.dxftype()}")

#         layer_data[layer_name] = geojson.FeatureCollection(features)
#         print(f"Layer {layer_name} processed with {len(features)} features.")

#     with open(output_geojson_path, 'w', encoding='utf-8') as f:
#         geojson.dump(layer_data, f, indent=2, ensure_ascii=False)
#     print(f"GeoJSON saved to {output_geojson_path}")


# # 레이어 리스트와 파일 경로
# layer_list = [
#     'SBA001', 'SBA002', 'SBA003', 'SBA004', 'SBA900', 'SBA999',
#     'SBD001', 'SBD002', 'SBD003', 'SBD004', 'SB101', 'SB102', '제원', '하수제원'
# ]
# dwf_file_path = "C:/cadFile/convert/377090300.dxf"
# output_geojson_path = "C:/cadFile/convert/377090300_all_layers_fixed.geojson"

# extract_all_layers_to_geojson(dwf_file_path, layer_list, output_geojson_path)


'''통합'''

# import ezdxf
# import geojson
# from shapely.geometry import mapping, Point, LineString, Polygon

# def extract_all_layers_to_geojson(dwf_file, layer_list, output_geojson_path):
#     try:
#         dwg = ezdxf.readfile(dwf_file)
#     except Exception as e:
#         print(f"Error reading DWF file: {e}")
#         return

#     layer_data = {}
#     modelspace = dwg.modelspace()

#     for layer_name in layer_list:
#         features = []
#         for entity in modelspace:
#             if entity.dxf.layer == layer_name:
#                 # LINE 처리
#                 if entity.dxftype() == 'LINE':
#                     geometry = LineString([(entity.dxf.start.x, entity.dxf.start.y),
#                                            (entity.dxf.end.x, entity.dxf.end.y)])
#                     properties = {"type": "LINE", "layer": layer_name}
#                     features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

#                 # TEXT 처리
#                 elif entity.dxftype() == 'TEXT':
#                     geometry = Point(entity.dxf.insert.x, entity.dxf.insert.y)
#                     properties = {
#                         "type": "TEXT",
#                         "layer": layer_name,
#                         "text": entity.dxf.text,
#                         "height": entity.dxf.height,
#                     }
#                     features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

#                 # INSERT 처리
#                 elif entity.dxftype() == 'INSERT':
#                     block_name = entity.dxf.name
#                     print(f"INSERT entity in layer {layer_name}, Block: {block_name}")
#                     block = dwg.blocks.get(block_name)
#                     for sub_entity in block:
#                         if sub_entity.dxftype() == 'LINE':
#                             geometry = LineString([(sub_entity.dxf.start.x, sub_entity.dxf.start.y),
#                                                    (sub_entity.dxf.end.x, sub_entity.dxf.end.y)])
#                             properties = {"type": "LINE", "layer": layer_name, "block": block_name}
#                             features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))
#                         elif sub_entity.dxftype() == 'TEXT':
#                             geometry = Point(sub_entity.dxf.insert.x, sub_entity.dxf.insert.y)
#                             properties = {
#                                 "type": "TEXT",
#                                 "layer": layer_name,
#                                 "block": block_name,
#                                 "text": sub_entity.dxf.text,
#                                 "height": sub_entity.dxf.height,
#                             }
#                             features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))
#                         elif sub_entity.dxftype() == 'LWPOLYLINE':
#                             points = [(point[0], point[1]) for point in sub_entity.get_points()]
#                             geometry = LineString(points)
#                             properties = {"type": "LWPOLYLINE", "layer": layer_name, "block": block_name}
#                             features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))
#                         else:
#                             print(f"Unsupported sub-entity type in block {block_name}: {sub_entity.dxftype()}")

#                 # CIRCLE 처리
#                 elif entity.dxftype() == 'CIRCLE':
#                     geometry = Point(entity.dxf.center.x, entity.dxf.center.y).buffer(entity.dxf.radius)
#                     properties = {"type": "CIRCLE", "layer": layer_name, "radius": entity.dxf.radius}
#                     features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

#                 # LWPOLYLINE 처리
#                 elif entity.dxftype() == 'LWPOLYLINE':
#                     points = [(point[0], point[1]) for point in entity.get_points()]
#                     geometry = LineString(points)
#                     properties = {"type": "LWPOLYLINE", "layer": layer_name}
#                     features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

#                 else:
#                     print(f"Unsupported entity type: {entity.dxftype()} in layer {layer_name}")

#         layer_data[layer_name] = geojson.FeatureCollection(features)
#         print(f"Layer {layer_name} processed with {len(features)} features.")

#     with open(output_geojson_path, 'w', encoding='utf-8') as f:
#         geojson.dump(layer_data, f, indent=2, ensure_ascii=False)
#     print(f"GeoJSON saved to {output_geojson_path}")


# # 레이어 리스트와 파일 경로
# layer_list = [
#     'SBA001', 'SBA002', 'SBA003', 'SBA004', 'SBA900', 'SBA999',
#     'SBD001', 'SBD002', 'SBD003', 'SBD004', 'SB101', 'SB102', '제원', '하수제원'
# ]
# dwf_file_path = "C:/cadFile/convert/377090300.dxf"
# output_geojson_path = "C:/cadFile/convert/377090300_all_layers_fixed.geojson"

# extract_all_layers_to_geojson(dwf_file_path, layer_list, output_geojson_path)


'''통합 2'''

import ezdxf
import geojson
from shapely.geometry import mapping, Point, LineString
from ezdxf.math import Matrix44

def apply_transformation(matrix, point):
    """
    변환 행렬(matrix)을 점(point)에 적용하여 전역 좌표 계산.
    """
    if len(point) == 2:  # 2D 좌표일 경우
        point = (point[0], point[1], 0)
    transformed_point = matrix.transform(point)
    return transformed_point.x, transformed_point.y

def extract_all_layers_to_geojson(dwf_file, layer_list, output_geojson_path):
    try:
        dwg = ezdxf.readfile(dwf_file)
    except Exception as e:
        print(f"Error reading DWF file: {e}")
        return

    layer_data = {}
    modelspace = dwg.modelspace()

    for layer_name in layer_list:
        features = []
        for entity in modelspace:
            if entity.dxf.layer == layer_name:
                # LINE 처리
                if entity.dxftype() == 'LINE':
                    geometry = LineString([(entity.dxf.start.x, entity.dxf.start.y),
                                           (entity.dxf.end.x, entity.dxf.end.y)])
                    properties = {"type": "LINE", "layer": layer_name}
                    features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

                # TEXT 처리
                elif entity.dxftype() == 'TEXT':
                    geometry = Point(entity.dxf.insert.x, entity.dxf.insert.y)
                    properties = {
                        "type": "TEXT",
                        "layer": layer_name,
                        "text": entity.dxf.text,
                        "height": entity.dxf.height,
                    }
                    features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))
                # CIRCLE 처리
                elif entity.dxftype() == 'CIRCLE':
                    geometry = Point(entity.dxf.center.x, entity.dxf.center.y).buffer(entity.dxf.radius)
                    properties = {"type": "CIRCLE", "layer": layer_name, "radius": entity.dxf.radius}
                    features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

                # LWPOLYLINE 처리
                elif entity.dxftype() == 'LWPOLYLINE':
                    points = [(point[0], point[1]) for point in entity.get_points()]
                    geometry = LineString(points)
                    properties = {"type": "LWPOLYLINE", "layer": layer_name}
                    features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

                # INSERT 처리
                elif entity.dxftype() == 'INSERT':
                    block_name = entity.dxf.name
                    print(f"INSERT entity in layer {layer_name}, Block: {block_name}")
                    block = dwg.blocks.get(block_name)
                    transformation_matrix = Matrix44(entity.matrix44())  # 변환 행렬 생성

                    for sub_entity in block:
                        # LINE 변환
                        if sub_entity.dxftype() == 'LINE':
                            start = apply_transformation(transformation_matrix, sub_entity.dxf.start)
                            end = apply_transformation(transformation_matrix, sub_entity.dxf.end)
                            geometry = LineString([start, end])
                            properties = {"type": "LINE", "layer": layer_name, "block": block_name}
                            features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

                        # TEXT 변환
                        elif sub_entity.dxftype() == 'TEXT':
                            insert = apply_transformation(transformation_matrix, sub_entity.dxf.insert)
                            geometry = Point(insert)
                            properties = {
                                "type": "TEXT",
                                "layer": layer_name,
                                "block": block_name,
                                "text": sub_entity.dxf.text,
                                "height": sub_entity.dxf.height,
                            }
                            features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

                        # LWPOLYLINE 변환
                        elif sub_entity.dxftype() == 'LWPOLYLINE':
                            points = [apply_transformation(transformation_matrix, point[:2])  # 2D 좌표로 변환
                                      for point in sub_entity.get_points()]
                            geometry = LineString(points)
                            properties = {"type": "LWPOLYLINE", "layer": layer_name, "block": block_name}
                            features.append(geojson.Feature(geometry=mapping(geometry), properties=properties))

                        else:
                            print(f"Unsupported sub-entity type in block {block_name}: {sub_entity.dxftype()}")

        layer_data[layer_name] = geojson.FeatureCollection(features)
        print(f"Layer {layer_name} processed with {len(features)} features.")

    with open(output_geojson_path, 'w', encoding='utf-8') as f:
        geojson.dump(layer_data, f, indent=2, ensure_ascii=False)
    print(f"GeoJSON saved to {output_geojson_path}")


# 레이어 리스트와 파일 경로
layer_list = [
    'SBA001', 'SBA002', 'SBA003', 'SBA004', 'SBA900', 'SBA999',
    'SBD001', 'SBD002', 'SBD003', 'SBD004', 'SB101', 'SB102', '제원', '하수제원'
]
dwf_file_path = "C:/cadFile/convert/377090200.dxf"
output_geojson_path = "C:/cadFile/convert/377090200_layers.geojson"

extract_all_layers_to_geojson(dwf_file_path, layer_list, output_geojson_path)
