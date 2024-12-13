'''
CAD FILE (.dxf) 파일 -> 원하는 LAYER 속성정보 추출 SAVE(.geojson)

'''

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

import os
#dxf 파일 경로
folder_dir = "C:/cadFile/DXF"
#dxf 파일 이름 리스트
fileNameList =os.listdir(folder_dir)

for fileName in fileNameList:
    name =fileName.split('.')[0]
    
    #입력 dxf파일 경로
    dwf_file_path = "C:/cadFile/DXF/{0}.dxf".format(name)
    #출력 폴더 경로
    output_geojson_path = "C:/cadFile/Layer/{0}_layers.geojson".format(name)
    
    extract_all_layers_to_geojson(dwf_file_path, layer_list, output_geojson_path)

