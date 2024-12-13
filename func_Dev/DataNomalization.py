import geopandas as gpd
from geopandas import GeoDataFrame

import pandas as pd
import json

from pyproj import Transformer

class DataNomalization:
    def __init__(self,propertyPath, pipePath):
        self.propertyPath = propertyPath
        self.pipePath = pipePath

        self.propertyDict =self.load_property()
        self.pipeData =self.load_pipe()
        self.pipeList = self.join_data()                  #속성정보 + 파이프정보

        self.relation_groupList = self.groupList()
        self.coords_epsg4326 =self.coordsEpsg4326()

    #속성정보 불러오기
    def load_property(self):
        property_geo_str=json.load(open(self.propertyPath, encoding='utf-8'))
        propertyDict = {}
        for coord in property_geo_str['features']:
            propertyDict[coord['properties']['fid']]=coord['properties']['text']
        return propertyDict
    
    #파이프 정보 불러오기
    def load_pipe(self):
        cen_str=json.load(open(self.pipePath, encoding='utf-8'))
        pipeData = cen_str['features']
        self.pipeData = pipeData
        return pipeData
    
    #파이프 - 속성 조합
    def join_data(self):
        propertyDict = self.load_property()
        pipeData = self.load_pipe()
        pipeList= []
        for feature in pipeData:
            pipeList.append({'fid':feature['properties']['fid'], 'coord':feature['geometry']['coordinates'], 'depth': propertyDict[feature['properties']['fid']].split('/')[4].replace('D','')})
        self.pipeList = pipeList
        return pipeList
    

    '''
        그룹관련함수
    '''
    #시작점인지 체크 :시작점(True), 중간점(False)
    def checkFirstPoint(self,first_point):
        for idx, val in enumerate(self.pipeList):
            comparison_coordinate = val['coord']
            comparison_last_point  = comparison_coordinate[len(comparison_coordinate)-1]
            if first_point[0]==comparison_last_point[0] and first_point[1]==comparison_last_point[1]:
                return False
        return True

    #비교
    def groupPoint(self,last_point):
        for idx, val in enumerate(self.pipeList):
            comparison_coordinate = val['coord']
            comparison_first_point  = comparison_coordinate[0]
            if comparison_first_point[0]==last_point[0] and comparison_first_point[1]==last_point[1]:
                return idx
        return False
    
    #순서 찾기
    def groupList(self):
        relation_groupList =[]
        for i, pipelist in enumerate(self.pipeList):
            current_coordinate = pipelist['coord']
            current_idx = i 
            current_last_point  = current_coordinate[len(current_coordinate)-1]
            current_first_point = current_coordinate[0]

            #시작점인지 판별
            isStartPoint = self.checkFirstPoint(current_first_point)
            if isStartPoint ==True:
                #그루핑 시작!!
                temp=[]
                temp.append(self.pipeList[current_idx])
                # pipeList.pop(current_idx)
                isValue = self.groupPoint(current_last_point)    #다음 좌표가 있는 지확인
                while(1):
                    if isValue ==False:
                        break
                    else:
                        temp.append(self.pipeList[isValue])      #isValue index
                        isValue = self.groupPoint(self.pipeList[isValue]['coord'][len(self.pipeList[isValue]['coord'])-1])
                relation_groupList.append(temp)

        # #coodinate이 z값에 depth 대입
        # for data in relation_groupList:
        #     for d in data:
        #         for c in d['coord']:
        #             c[2] = float(d['depth'])

        #depth 추가시 그룹의 다음 depth를 비교해서 비율 조정
        for data in relation_groupList:
            for i in range(len(data)-1):
                if i+1 <= len(data)-1:
                    resentDepth = float(data[i]['depth'])
                    nextDepth = float(data[i+1]['depth'])
                    radio = abs((nextDepth - resentDepth)/ len(data[i]['coord']))
                    for idx,c in enumerate(data[i]['coord']):
                        c[2] = float(data[i]['depth']) -(radio*(idx+1))
                else:
                    for c in data[i]['coord']:
                        c[2] = float(data[i]['depth'])
        
        return relation_groupList
    
    # def toEpsg4326():
    #     transformer = Transformer.from_crs("EPSG:5186", "EPSG:4326", always_xy=True)
    #     return transformer
    
    def coordsEpsg4326(self, coord=[]):
        transformer = Transformer.from_crs("EPSG:5186", "EPSG:4326", always_xy=True)
        if coord ==[]:
            coords_epsg5186 =[]
            for data in self.relation_groupList:
                temp =[]
                for d in data:
                    for p in d['coord']:
                        temp.append(p)
                coords_epsg5186.append(temp)
            coords_epsg4326 = []
            for group in coords_epsg5186:
                converted_group = []
                for point in group:
                    x, y, z = point  # x, y는 좌표, z는 그대로 유지
                    lon, lat = transformer.transform(x, y)  # 좌표 변환
                    converted_group.append([lon, lat, z])  # 변환된 좌표 추가
                coords_epsg4326.append(converted_group)
            self.coords_epsg4326 =coords_epsg4326
            return coords_epsg4326
        
        else:
            coords_epsg4326 = []
            for group in coord:
                converted_group = []
                for point in group:
                    x, y, z = point  # x, y는 좌표, z는 그대로 유지
                    lon, lat = transformer.transform(x, y)  # 좌표 변환
                    converted_group.append([lon, lat, z])  # 변환된 좌표 추가
                coords_epsg4326.append(converted_group)
            self.coords_epsg4326 =coords_epsg4326
            return coords_epsg4326


    def saveData(self,fileName,filePath=''):
        #데이터 저장
        coords_wgs84_json = {'coord':self.coords_epsg4326}

        if filePath =='':
            file_Path ="{0}.json".format(fileName)
            with open(file_Path, 'w') as f:
                json.dump(coords_wgs84_json,f)
        else:
            file_Path = "{0}/{1}.json".format(file_Path,fileName)   
            with open(file_Path, 'w') as f:
                json.dump(coords_wgs84_json,f)