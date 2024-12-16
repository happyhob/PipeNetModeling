import geopandas as gpd
from geopandas import GeoDataFrame

import pandas as pd
import json

from pyproj import Transformer
import os

import numpy as np
import json


#파일 정보 로드
def fileList(dir_path):
    folder_dir = dir_path
    fileNameList =os.listdir(folder_dir)
    return fileNameList

#인근 좌표 재원
def find_closest_points_with_lines(property_features, lines):
    """
    각 line과 해당 line에 가장 가까운 점의 `text` 값을 묶어서 반환.

    :property_features: property_str['features'] 형식의 리스트
    :lines: [
        [[x, y], [x, y], [x, y], ...],  # 첫 번째 line
        [[x, y], [x, y], [x, y], ...],  # 두 번째 line
        ...
    ]
    :return: [[[x, y], [x, y], ...], 가장 가까운 점의 `text` 값] 형식의 리스트
    """
    
    def point_to_segment_distance(point, segment):
        """
        점과 선분 사이의 최소 거리 계산
        :param point: [x, y]
        :param segment: [[x1, y1], [x2, y2]]
        :return: 점과 선분 사이의 거리
        """
        px, py = point
        (x1, y1), (x2, y2) = segment
        line_vec = np.array([x2 - x1, y2 - y1])
        point_vec = np.array([px - x1, py - y1])
        line_len_squared = np.dot(line_vec, line_vec)

        if line_len_squared == 0:
            return np.linalg.norm(point_vec)
        
        t = max(0, min(1, np.dot(point_vec, line_vec) / line_len_squared))
        closest_point = np.array([x1, y1]) + t * line_vec
        return np.linalg.norm(np.array([px, py]) - closest_point)

    results = []
    for line in lines:
        segments = [(line[i], line[i + 1]) for i in range(len(line) - 1)]
        closest_point_text = None
        min_distance = float('inf')

        # 각 segment에 대해 모든 property_features와 거리 계산
        for feature in property_features:
            point = feature['geometry']['coordinates']
            text = feature['properties']['text']  # `text` 값 추출
            for segment in segments:
                distance = point_to_segment_distance(point, segment)
                if distance < min_distance:
                    min_distance = distance
                    closest_point_text = text

        # 각 line과 가장 가까운 점의 `text`를 묶어서 저장
        results.append([line, closest_point_text])
    
    return results

# #epsg 5186 -> 4325
def convertEpsg(coord):
    transformer = Transformer.from_crs("EPSG:5186", "EPSG:4326", always_xy=True)
    coords_epsg4326=[]
    for group in coord:
        converted_group = []
        for point in group:
            x, y, z = point  # x, y는 좌표, z는 그대로 유지
            lon, lat = transformer.transform(x, y)  # 좌표 변환
            converted_group.append([lon, lat, z])  # 변환된 좌표 추가
        coords_epsg4326.append(converted_group)
    return coords_epsg4326

def checkFirstPoint(coordinate,firstPoint):
    for idx,comperison_coord in enumerate(coordinate):
        comperison_lastPoint = comperison_coord[len(comperison_coord)-1]
        if firstPoint[0]==comperison_lastPoint[0] and firstPoint[1]==comperison_lastPoint[1]:
            return False
    return True
def checkGroupPoint(coordinate, lastPoint):
    for idx, current_coord in enumerate(coordinate):
        comparison_points = current_coord[0]
        if comparison_points[0]==lastPoint[0] and comparison_points[1] == lastPoint[1]:
            return idx
    return False
    

    

#레이어 아이디 정보
layer_list = [
    'SBA001', 'SBA002', 'SBA003', 'SBA004', 'SBA900', 'SBA999',
    'SBD001', 'SBD002', 'SBD003', 'SBD004', 'SB101', 'SB102', '제원', '하수제원', '관라벨'
]

#geojson list
fileName_list = fileList('C:/cadFile/Layer')


for idx, file in enumerate(fileName_list):
    resultData =[]
    CadData_Path = "C:/cadFile/Layer/{0}".format(file)  #377090200_layers.geojson
    cadData = json.load(open(CadData_Path,encoding='utf-8'))

    #제원정보
    specifications_data = (cadData.get('제원', {}).get('features') or
                       cadData.get('하수제원', {}).get('features') or 
                       cadData.get('관라벨', {}).get('features')) 

    #filtering
    for idx, layerId in enumerate(layer_list):
        #레이어 정보 없음
        if len(cadData[layerId]['features'])==0:
            continue
        elif 'SBA' in layerId:
            SBAData =[]
            for data in cadData[layerId]['features']:
                SBAData.append(data['geometry']['coordinates'])

            lineData = find_closest_points_with_lines(specifications_data, SBAData)
            
            epsg5184_coord =[]  #3차원 배열
            for line in lineData:
                coordinates = line[0]
                specifications = line[1]
                try:
                    parts = specifications.split('/')
                    last_part = parts[-1].replace('D', '')
                    depth = float(last_part)
                except ValueError:
                    # 변환 실패 시 처리: 기본값 설정 또는 로그 출력
                    depth = 0.0  # 예시로 기본값 0.0 설정
                for coord in coordinates:
                    coord.append(depth)
                epsg5184_coord.append(coordinates)

            '''group 로직 수행'''
            dataList = []
            for idx, current_coord in enumerate(epsg5184_coord):
                first_coord = current_coord[0]
                last_coord = current_coord[len(current_coord)-1]

                isStartPoint = checkFirstPoint(epsg5184_coord,first_coord)
                if isStartPoint: #시작점이다.
                    temp = []
                    temp.append(current_coord)
                    isGroup = checkGroupPoint(epsg5184_coord,last_coord)
                    while(1):
                        if isGroup ==False:
                            break
                        else:
                            temp.append(epsg5184_coord[isGroup])
                            isGroup = checkGroupPoint(epsg5184_coord, epsg5184_coord[isGroup][len(epsg5184_coord[isGroup])-1])
                    dataList.append(temp)
            print(dataList)

            coords_epsg4326 = convertEpsg(epsg5184_coord)


            id = '{0}_{1}'.format(file.split('.')[0],layerId)
            coords_wgs84_json = {'id':id, 'coord':coords_epsg4326}
            resultData.append(coords_wgs84_json)
        else:
            continue

    file_Path ="C:/Users/magpie/Desktop/pipe프로젝트관련/PipeData_Create/data/{0}.json".format(file.split('.')[0])
    with open(file_Path, 'w') as f:
        json.dump(resultData,f)