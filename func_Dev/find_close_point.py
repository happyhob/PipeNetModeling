# import numpy as np
# import json

# def find_closest_points_with_lines(property_points, lines):
#     """
#     각 line과 해당 line에 가장 가까운 점을 묶어서 반환.

#     :property_points: [[x, y], [x, y], ...] 형식의 점 리스트
#     :lines: [
#         [[x, y], [x, y], [x, y], ...],  # 첫 번째 line
#         [[x, y], [x, y], [x, y], ...],  # 두 번째 line
#         ...
#     ]
#     :return: [[[x, y], [x, y], ...], [가장 가까운 점]] 형식의 리스트
#     """
    
#     def point_to_segment_distance(point, segment):
#         """
#         점과 선분 사이의 최소 거리 계산
#         :param point: [x, y]
#         :param segment: [[x1, y1], [x2, y2]]
#         :return: 점과 선분 사이의 거리
#         """
#         px, py = point
#         (x1, y1), (x2, y2) = segment
#         line_vec = np.array([x2 - x1, y2 - y1])     #선분의 방향 벡터
#         point_vec = np.array([px - x1, py - y1])    # 선분의 식작점에서 점까지의 벡터
#         line_len_squared = np.dot(line_vec, line_vec)

#         if line_len_squared == 0:
#             return np.linalg.norm(point_vec)    #point_vec의 크기 계산      루트(x**2 +y**2)
        
#         ''' 투영계산
#             t는 point가 선분 위 어디에 두영되는지 결정
#             t=0, 선분의 시작점이 가장 가까운 점
#             t=1, 선분의 끝점이 가장 가까운 점
#         '''
#         t = max(0, min(1, np.dot(point_vec, line_vec) / line_len_squared))
#         #선분 위의 가장 가까운 점
#         closest_point = np.array([x1, y1]) + t * line_vec
#         # point와 closest_point 간의 거리 계산
#         return np.linalg.norm(np.array([px, py]) - closest_point)

#     results = []
#     for line in lines:
#         # 각 line을 segments로 나눔 ex)[[0, 0], [10, 0], [10, 10]] → [[[0, 0], [10, 0]], [[10, 0], [10, 10]]].
#         segments = [(line[i], line[i + 1]) for i in range(len(line) - 1)]
#         closest_point = None
#         min_distance = float('inf') #무한대 초기 설정값

#         # 각 segment에 대해 모든 property_points와 거리 계산:
#         for point in property_points:
#             for segment in segments:
#                 distance = point_to_segment_distance(point, segment)
#                 # 최소 거리와 가장 가까운 점 갱신:
#                 if distance < min_distance:
#                     min_distance = distance
#                     closest_point = point

#         # 각 line과 가장 가까운 점을 묶어서 저장
#         results.append([line, closest_point])
    
#     return results


# # 데이터
# property_points = [[5, 2], [15, 5], [8, 7], [1, 1]]
# lines = [
#     [[0, 0], [10, 0], [10, 10], [0, 10]],
#     [[20, 20], [30, 20], [30, 30]]
# ]

# # 실행
# # closest_points_with_lines = find_closest_points_with_lines(property_points, lines)
# # print("가장 가까운 점과 line 묶음:")
# # for line_and_point in closest_points_with_lines:
# #     print(line_and_point)





# SBA001_Path = "C:/cadFile/convert/SBA001.geojson"
# SBA001_str=json.load(open(SBA001_Path, encoding='utf-8'))
# SBA_LIST =[]

# for data in SBA001_str['features']:
#     SBA_LIST.append(data['geometry'] ['coordinates'])


# property_Path = "C:/cadFile/convert/제원.geojson"
# property_str=json.load(open(property_Path, encoding='utf-8'))
# property_LIST =[]

# for data in property_str['features']:
#     property_LIST.append(data['geometry'] ['coordinates'])


# # print(SBA_LIST)
# # print(property_LIST)



# closest_points_with_lines = find_closest_points_with_lines(property_LIST, SBA_LIST)
# print(closest_points_with_lines[0])




import numpy as np
import json

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


# 데이터 로드
SBA001_Path = "C:/cadFile/convert/SBA001.geojson"
SBA001_str = json.load(open(SBA001_Path, encoding='utf-8'))
SBA_LIST = [data['geometry']['coordinates'] for data in SBA001_str['features']]

property_Path = "C:/cadFile/convert/제원.geojson"
property_str = json.load(open(property_Path, encoding='utf-8'))
property_features = property_str['features']  # 전체 `features` 리스트

# 실행
closest_points_with_lines = find_closest_points_with_lines(property_features, SBA_LIST)
#closest_points_with_lines = [[[coord],[text]],,,,]

# 결과 출력
for data in closest_points_with_lines:
    print(data[1])
