import geopandas as gpd
from geopandas import GeoDataFrame

import pandas as pd
import json

from pyproj import Transformer



#속성 정보 불러오기
property_geo = 'C:/Users/magpie/Desktop/pipePython/data/오수관_속성ID.geojson'
property_geo_str=json.load(open(property_geo, encoding='utf-8'))
propertyDict = {}
for coord in property_geo_str['features']:
    propertyDict[coord['properties']['fid']]=coord['properties']['text']

# propertyDict[109].split('/')[4].replace('D','')


#파이프관 정보 불러오기
state_geo = 'C:/Users/magpie/Desktop/pipePython/data/오수관.geojson'
cen_str=json.load(open(state_geo, encoding='utf-8'))
pipeList = []

for feature in cen_str['features']:
    pipeList.append({'fid':feature['properties']['fid'], 'coord':feature['geometry']['coordinates'], 'depth': propertyDict[feature['properties']['fid']].split('/')[4].replace('D','')})

#시작점인지 체크 :시작점(True), 중간점(False)
def checkFirstPoint(first_point):
    for idx, val in enumerate(pipeList):
        comparison_coordinate = val['coord']
        comparison_last_point  = comparison_coordinate[len(comparison_coordinate)-1]
        if first_point[0]==comparison_last_point[0] and first_point[1]==comparison_last_point[1]:
            return False
    return True

#비교
def groupPoint(last_point):
    for idx, val in enumerate(pipeList):
        comparison_coordinate = val['coord']
        comparison_first_point  = comparison_coordinate[0]
        if comparison_first_point[0]==last_point[0] and comparison_first_point[1]==last_point[1]:
            return idx
    return False


#최종 데이터
dataList =[]
for i, pipelist in enumerate(pipeList):
    current_coordinate = pipelist['coord']
    current_idx = i 
    current_last_point  = current_coordinate[len(current_coordinate)-1]
    current_first_point = current_coordinate[0]
    
    #시작점인지 판별
    isStartPoint = checkFirstPoint(current_first_point)
    if isStartPoint ==True:
        #그루핑 시작!!
        temp=[]
        temp.append(pipeList[current_idx])
        # pipeList.pop(current_idx)
        isValue = groupPoint(current_last_point)    #다음 좌표가 있는 지확인
        while(1):
            if isValue ==False:
                break
            else:
                temp.append(pipeList[isValue])      #isValue index
                isValue = groupPoint(pipeList[isValue]['coord'][len(pipeList[isValue]['coord'])-1])
        dataList.append(temp)
    



#coodinate이 z값에 depth 대입
for data in dataList:
    for d in data:
        for c in d['coord']:
            c[2] = float(d['depth'])

print(dataList)


coords_epsg5186 =[]
for data in dataList:
    temp =[]
    for d in data:
        for p in d['coord']:
            temp.append(p)
    coords_epsg5186.append(temp)

print(coords_epsg5186)


coords_wgs84 = []


transformer = Transformer.from_crs("EPSG:5186", "EPSG:4326", always_xy=True)
for group in coords_epsg5186:
    converted_group = []
    for point in group:
        x, y, z = point  # x, y는 좌표, z는 그대로 유지
        lon, lat = transformer.transform(x, y)  # 좌표 변환
        converted_group.append([lon, lat, z])  # 변환된 좌표 추가
    coords_wgs84.append(converted_group)

print(coords_wgs84)



coords_wgs84_json = {'coord':coords_wgs84}

file_Path ='오수관데이터.json'
with open(file_Path, 'w') as f:
    json.dump(coords_wgs84_json,f)

