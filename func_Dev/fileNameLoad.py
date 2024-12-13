import os

folder_dir = "C:/cadFile/DXF"

fileNameList =os.listdir(folder_dir)

for fileName in fileNameList:
    name =fileName.split('.')[0]
    print(name)

