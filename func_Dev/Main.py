import DataNomalization


property_geo = 'C:/Users/magpie/Desktop/pipePython/data/유수관_속성ID.geojson'
state_geo = 'C:/Users/magpie/Desktop/pipePython/data/유수관.geojson'



Data = DataNomalization.DataNomalization(property_geo,state_geo)


''' 그루핑 하지 않은 데이터'''
def OriginData():
    temp =[]
    DataList = Data.join_data()

    for data in DataList:
        coord = data['coord']
        depth = data['depth']
        for point in coord:
            point[2] = float(depth)
        temp.append(data['coord'])


    print(Data.coordsEpsg4326(temp))
    Data.saveData('OriginData')
OriginData()