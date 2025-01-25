import shapefile as sp
import requests as re
import json
import pandas as pd
import time

def poibian1(key:str, bianjiestr:str,guanjianci:str,leixing:str)->dict:
    canshu = {'key':key,'polygon':bianjiestr,'types':leixing,'keywords':guanjianci,'page_size':'25', 'show_fields': 'children,business,indoor,navi,photos'}
    res1 = re.get("https://restapi.amap.com/v5/place/polygon?parameters",params=canshu)
    res2 = json.loads(res1.text)
    #print(res2)
    return res2

def poibian0(key:str, bianjiestr:str,guanjianci:str,leixing:str)->dict:
    canshu = {'key':key,'polygon':bianjiestr,'types':leixing,'keywords':guanjianci,'page_size':'25'}
    res1 = re.get("https://restapi.amap.com/v5/place/polygon?parameters",params=canshu)
    res2 = json.loads(res1.text)
    #print(res2)
    return res2

def Judge1(key:str,ax:float,ay:float,bx:float,by:float,guanjianci:str,leixing:str):
    bianjielist = []
    bianjielist.append(str(ax))
    bianjielist.append(',')
    bianjielist.append(str(ay))
    bianjielist.append('|')
    bianjielist.append(str(bx))
    bianjielist.append(',')
    bianjielist.append(str(by))
    bianjiestr = ''.join(bianjielist)
    res1 = poibian1(key, bianjiestr, guanjianci, leixing)
    count = len(res1['pois'])
    if int(count) >= 25:
        print(count,"no")
        return 0
    else:
        print(count,"yes")
        return res1

def Judge0(key:str,ax:float,ay:float,bx:float,by:float,guanjianci:str,leixing:str):
    bianjielist = []
    bianjielist.append(str(ax))
    bianjielist.append(',')
    bianjielist.append(str(ay))
    bianjielist.append('|')
    bianjielist.append(str(bx))
    bianjielist.append(',')
    bianjielist.append(str(by))
    bianjiestr = ''.join(bianjielist)
    res1 = poibian0(key, bianjiestr, guanjianci, leixing)
    count = len(res1['pois'])
    if int(count) >= 25:
        print(count,"no")
        return 0
    else:
        print(count,"yes")
        return res1

def bianma(key: str,address :str)->dict:#获取地理编码
    canshu = {'key':key,'address':address}
    res1 = re.get("https://restapi.amap.com/v3/geocode/geo?parameters",params=canshu)
    res2 = json.loads(res1.text)
    return res2#直接返回标准化的获取值

def poidian1(key:str,zuobiao:str,banjing:str,guanjianci:str,leixing:str)->dict:
    canshu = {'key': key, 'location': zuobiao, 'radius': banjing, 'keywords': guanjianci, 'types': leixing, 'page_size': '25', 'show_fields': 'children,business,navi,photos'}
    res1 = re.get("https://restapi.amap.com/v5/place/around?parameters", params=canshu)
    res2 = json.loads(res1.text)
    return res2

def poidian0(key:str,zuobiao:str,banjing:str,guanjianci:str,leixing:str)->dict:
    canshu = {'key': key, 'location': zuobiao, 'radius': banjing, 'keywords': guanjianci, 'types': leixing, 'page_size': '25'}
    res1 = re.get("https://restapi.amap.com/v5/place/around?parameters", params=canshu)
    res2 = json.loads(res1.text)
    return res2

gongneng = int(input('选择你需要的功能，依据需要的功能输入对应数字并按回车：获取地理编码/按半径查询POI/按shp查询POI：1/2/3\n注：要获取大于25个点的数据请用“按shp查询POI”\n'))
key = input('请输入你的key\n')
flag = 0
print('如果下面某项不需要填写的话按回车即可')
if gongneng == 1:
    flag = 1
    while flag == 1:
        yuanshi = pd.DataFrame({})
        CurBianma = bianma(key,input('输入你要查询的地点（尽量填写结构化地址信息:省份＋城市＋区县＋城镇＋乡村＋街道＋门牌号码+关键词）\n示例：成都市成华区二仙桥东三路1号成都理工大学\n'))
        ResBianma = {'名称': [], '等级': [], '坐标': [], '城市': [], '区县': []}
        yuanshi = pd.concat([yuanshi, pd.DataFrame(CurBianma)], ignore_index=True)
        for i in range(0,len(CurBianma['geocodes'])):
            ResBianma['名称'].append(CurBianma['geocodes'][i]['formatted_address'])
            ResBianma['等级'].append(CurBianma['geocodes'][i]['level'])
            ResBianma['坐标'].append(CurBianma['geocodes'][i]['location'])
            ResBianma['城市'].append(CurBianma['geocodes'][i]['city'])
            ResBianma['区县'].append(CurBianma['geocodes'][i]['district'])
            print('第',i+1,'项 名称：',ResBianma['名称'][i],' 等级：',ResBianma['等级'][i],' 坐标：',ResBianma['坐标'][i],' 城市：',ResBianma['城市'][i],' 区县：',ResBianma['区县'][i])
        flag = int(input('是否再次查询（1/0）\n'))
        shuchu = pd.DataFrame(ResBianma)
        shuchu.to_excel('地理编码.xlsx', sheet_name='全部', index=False)
        yuanshi.to_excel('地理编码_原始获取.xlsx', sheet_name='全部', index=False)
        print('输出结果已生成在程序根目录下的“地理编码.xlsx”文件\n原始获取数据已生成在程序根目录下的“地理编码_原始获取.xlsx”文件')
elif gongneng == 2:
    flag = 1
    while flag == 1:
        yuanshi = pd.DataFrame({})
        zuobiao = input('输入目标经纬度\n')
        banjing = input('输入搜索半径（米）\n')
        #zuobiao = '104.14753100,30.67501200'
        #banjing = '1000'
        guanjianci = input('输入关键词（只支持一个）\n')
        leixing = input('输入你需要的POI类型（参考POI分类编码和城市编码表;多个类型用“|”分割;默认指定餐饮服务、生活服务、商务住宅）\n')
        if int(input('是否需要详细信息（1/0）\n')) == 1:
            CurDian = poidian1(key, zuobiao, banjing, guanjianci, leixing)
            yuanshi = pd.concat([yuanshi, pd.DataFrame(CurDian)], ignore_index=True)
            ResDian = {'poi 名称': [], 'poi 唯一标识': [], 'poi 经纬度': [], 'poi 所属类型': [], 'poi 分类编码': [], 'poi 所属省份': [],'poi 所属城市': [],'poi 所属区县': [],
                       'poi 详细地址': [],'poi 所属省份编码': [],'poi 所属区域编码': [],'poi 所属城市编码': [],
                       '子 poi 唯一标识': [],'子 poi 名称': [],'子 poi 经纬度': [],'子 poi 详细地址': [],'子 poi 所属类型': [],'子 poi 分类编码': [],
                       'poi 所属商圈': [],'poi 的联系电话': [],'poi 特色内容': [],'poi 评分': [],'poi 人均消费': [],'停车场类型': [],'poi 的别名': [],
                       'poi 对应的导航引导点坐标': [],'poi 的入口经纬度坐标': [],'poi 的出口经纬度坐标': [],'poi 的地理格 id': [],'poi 的图片介绍': [],'poi 图片的下载链接': []}
            print(CurDian)
            for i in range(0, len(CurDian['pois'])):
                ResDian['poi 名称'].append(CurDian['pois'][i]['name'])
                ResDian['poi 唯一标识'].append(CurDian['pois'][i]['id'])
                ResDian['poi 经纬度'].append(CurDian['pois'][i]['location'])
                ResDian['poi 所属类型'].append(CurDian['pois'][i]['type'])
                ResDian['poi 分类编码'].append(CurDian['pois'][i]['typecode'])
                ResDian['poi 所属省份'].append(CurDian['pois'][i]['pname'])
                ResDian['poi 所属城市'].append(CurDian['pois'][i]['cityname'])
                ResDian['poi 所属区县'].append(CurDian['pois'][i]['adname'])
                ResDian['poi 详细地址'].append(CurDian['pois'][i]['address'])
                ResDian['poi 所属省份编码'].append(CurDian['pois'][i]['pcode'])
                ResDian['poi 所属区域编码'].append(CurDian['pois'][i]['adcode'])
                ResDian['poi 所属城市编码'].append(CurDian['pois'][i]['citycode'])
                try:
                    ResDian['子 poi 唯一标识'].append(CurDian['pois'][i]['children']['id'])
                except:
                    ResDian['子 poi 唯一标识'].append('')
                try:
                    ResDian['子 poi 名称'].append(CurDian['pois'][i]['children']['name'])
                except:
                    ResDian['子 poi 名称'].append('')
                try:
                    ResDian['子 poi 经纬度'].append(CurDian['pois'][i]['children']['location'])
                except:
                    ResDian['子 poi 经纬度'].append('')
                try:
                    ResDian['子 poi 详细地址'].append(CurDian['pois'][i]['children']['address'])
                except:
                    ResDian['子 poi 详细地址'].append('')
                try:
                    ResDian['子 poi 所属类型'].append(CurDian['pois'][i]['children']['subtype'])
                except:
                    ResDian['子 poi 所属类型'].append('')
                try:
                    ResDian['子 poi 分类编码'].append(CurDian['pois'][i]['children']['typecode'])
                except:
                    ResDian['子 poi 分类编码'].append('')
                try:
                    ResDian['poi 所属商圈'].append(CurDian['pois'][i]['business']['business_area'])
                except:
                    ResDian['poi 所属商圈'].append('')
                try:
                    ResDian['poi 的联系电话'].append(CurDian['pois'][i]['business']['tel'])
                except:
                    ResDian['poi 的联系电话'].append('')
                try:
                    ResDian['poi 特色内容'].append(CurDian['pois'][i]['business']['tag'])
                except:
                    ResDian['poi 特色内容'].append('')
                try:
                    ResDian['poi 评分'].append(CurDian['pois'][i]['business']['rating'])
                except:
                    ResDian['poi 评分'].append('')
                try:
                    ResDian['poi 人均消费'].append(CurDian['pois'][i]['business']['cost'])
                except:
                    ResDian['poi 人均消费'].append('')
                try:
                    ResDian['停车场类型'].append(CurDian['pois'][i]['business']['parking_type'])
                except:
                    ResDian['停车场类型'].append('')
                try:
                    ResDian['poi 的别名'].append(CurDian['pois'][i]['business']['alias'])
                except:
                    ResDian['poi 的别名'].append('')
                try:
                    ResDian['poi 对应的导航引导点坐标'].append(CurDian['pois'][i]['navi']['navi_poiid'])
                except:
                    ResDian['poi 对应的导航引导点坐标'].append('')
                try:
                    ResDian['poi 的入口经纬度坐标'].append(CurDian['pois'][i]['navi']['entr_location'])
                except:
                    ResDian['poi 的入口经纬度坐标'].append('')
                try:
                    ResDian['poi 的出口经纬度坐标'].append(CurDian['pois'][i]['navi']['exit_location'])
                except:
                    ResDian['poi 的出口经纬度坐标'].append('')
                try:
                    ResDian['poi 的地理格 id'].append(CurDian['pois'][i]['navi']['gridcode'])
                except:
                    ResDian['poi 的地理格 id'].append('')
                try:
                    ResDian['poi 的图片介绍'].append(CurDian['pois'][i]['photos'][0]['title'])
                except:
                    ResDian['poi 的图片介绍'].append('')
                try:
                    ResDian['poi 图片的下载链接'].append(CurDian['pois'][i]['photos'][0]['url'])
                except:
                    ResDian['poi 图片的下载链接'].append('')
                print('第', i + 1, '项 名称：', ResDian['poi 名称'][i],
                      ' 坐标：', ResDian['poi 经纬度'][i],
                      ' POI类型：', ResDian['poi 所属类型'][i],
                      ' 详细地址：', ResDian['poi 详细地址'][i],
                      ' 城市：', ResDian['poi 所属城市'][i],
                      ' 区县：', ResDian['poi 所属区县'][i])
            flag = int(input('是否再次查询（1/0）\n'))
            shuchu = pd.DataFrame(ResDian)
            shuchu.to_excel('按半径查询POI_详细信息.xlsx', sheet_name='全部', index=False)
            yuanshi.to_excel('按半径查询POI_详细信息_原始获取.xlsx', sheet_name='全部', index=False)
            print('输出结果已生成在程序根目录下的“按半径查询POI_详细信息.xlsx”文件\n原始获取数据已生成在程序根目录下的“按半径查询POI_详细信息_原始获取.xlsx”文件')
        else:
            CurDian = poidian0(key, zuobiao, banjing, guanjianci, leixing)
            yuanshi = pd.concat([yuanshi, pd.DataFrame(CurDian)], ignore_index=True)
            ResDian = {'名称': [], '坐标': [], 'POI类型': [], '详细地址': [], '城市': [], '区县': []}
            for i in range(0, len(CurDian['pois'])):
                ResDian['名称'].append(CurDian['pois'][i]['name'])
                ResDian['坐标'].append(CurDian['pois'][i]['location'])
                ResDian['POI类型'].append(CurDian['pois'][i]['type'])
                ResDian['详细地址'].append(CurDian['pois'][i]['address'])
                ResDian['城市'].append(CurDian['pois'][i]['cityname'])
                ResDian['区县'].append(CurDian['pois'][i]['adname'])
                print('第', i + 1, '项 名称：', ResDian['名称'][i],
                      ' 坐标：', ResDian['坐标'][i],
                      ' POI类型：', ResDian['POI类型'][i],
                      ' 详细地址：', ResDian['详细地址'][i],
                      ' 城市：', ResDian['城市'][i],
                      ' 区县：', ResDian['区县'][i])
            flag = int(input('是否再次查询（1/0）\n'))
            shuchu = pd.DataFrame(ResDian)
            shuchu.to_excel('按半径查询POI_简要信息.xlsx', sheet_name='全部', index=False)
            yuanshi.to_excel('按半径查询POI_简要信息_原始获取.xlsx', sheet_name='全部', index=False)
            print('输出结果已生成在程序根目录下的“按半径查询POI_简要信息.xlsx”文件\n原始获取数据已生成在程序根目录下的“按半径查询POI_简要信息_原始获取.xlsx”文件')
elif gongneng == 3:
    guanjianci = input('输入关键词\n')
    leixing = input('输入poi类型\n')
    input('在该程序同一文件夹内放置目标shp文件，文件名命名为“目标区域.shp”，坐标系要求为GCJ02。放完后直接按回车即可')
    MaxPol = sp.Reader('目标区域.shp')
    MaxPolBox = MaxPol.bbox
    MaxPolBoxFlo = [round(float(MaxPolBox[0]), 6), round(float(MaxPolBox[1]), 6), round(float(MaxPolBox[2]), 6),round(float(MaxPolBox[3]), 6)]
    ResPolList = []
    CurPolList = [MaxPolBoxFlo]
    len1 = len(CurPolList)
    i = 0
    yuanshi = pd.DataFrame({})
    if int(input('是否需要详细信息（1/0）\n')) == 1:
        ResList = {'poi 名称': [], 'poi 唯一标识': [], 'poi 经纬度': [], 'poi 所属类型': [], 'poi 分类编码': [], 'poi 所属省份': [],'poi 所属城市': [],'poi 所属区县': [],
                   'poi 详细地址': [],'poi 所属省份编码': [],'poi 所属区域编码': [],'poi 所属城市编码': [],
                   '子 poi 唯一标识': [],'子 poi 名称': [],'子 poi 经纬度': [],'子 poi 详细地址': [],'子 poi 所属类型': [],'子 poi 分类编码': [],
                   'poi 所属商圈': [],'poi 的联系电话': [],'poi 特色内容': [],'poi 评分': [],'poi 人均消费': [],'停车场类型': [],'poi 的别名': [],
                   '是否有室内地图标志': [],'所在建筑物的 POI ID': [],'楼层索引': [],'所在楼层': [],
                   'poi 对应的导航引导点坐标': [],'poi 的入口经纬度坐标': [],'poi 的出口经纬度坐标': [],'poi 的地理格 id': [],'poi 的图片介绍': [],'poi 图片的下载链接': []}
        while i < len1:
            ax = CurPolList[i][0]
            ay = CurPolList[i][1]
            bx = CurPolList[i][2]
            by = CurPolList[i][3]
            CurPol = Judge1(key, ax, ay, bx, by, guanjianci, leixing)
            if str(type(CurPol)) == "<class 'int'>":
                CurPolList.append([ax, ay, round((ax + bx) / 2, 6), round((ay + by) / 2, 6)])
                CurPolList.append([round((ax + bx) / 2, 6), ay, bx, round((ay + by) / 2, 6)])
                CurPolList.append([ax, round((ay + by) / 2, 6), round((ax + bx) / 2, 6), by])
                CurPolList.append([round((ax + bx) / 2, 6), round((ay + by) / 2, 6), bx, by])
            else:
                for j in range(0, len(CurPol['pois'])):
                    ResList['poi 名称'].append(CurPol['pois'][j]['name'])
                    ResList['poi 唯一标识'].append(CurPol['pois'][j]['id'])
                    ResList['poi 经纬度'].append(CurPol['pois'][j]['location'])
                    ResList['poi 所属类型'].append(CurPol['pois'][j]['type'])
                    ResList['poi 分类编码'].append(CurPol['pois'][j]['typecode'])
                    ResList['poi 所属省份'].append(CurPol['pois'][j]['pname'])
                    ResList['poi 所属城市'].append(CurPol['pois'][j]['cityname'])
                    ResList['poi 所属区县'].append(CurPol['pois'][j]['adname'])
                    ResList['poi 详细地址'].append(CurPol['pois'][j]['address'])
                    ResList['poi 所属省份编码'].append(CurPol['pois'][j]['pcode'])
                    ResList['poi 所属区域编码'].append(CurPol['pois'][j]['adcode'])
                    ResList['poi 所属城市编码'].append(CurPol['pois'][j]['citycode'])
                    try:
                        ResList['子 poi 唯一标识'].append(CurPol['pois'][j]['children']['id'])
                    except:
                        ResList['子 poi 唯一标识'].append('')
                    try:
                        ResList['子 poi 名称'].append(CurPol['pois'][j]['children']['name'])
                    except:
                        ResList['子 poi 名称'].append('')
                    try:
                        ResList['子 poi 经纬度'].append(CurPol['pois'][j]['children']['location'])
                    except:
                        ResList['子 poi 经纬度'].append('')
                    try:
                        ResList['子 poi 详细地址'].append(CurPol['pois'][j]['children']['address'])
                    except:
                        ResList['子 poi 详细地址'].append('')
                    try:
                        ResList['子 poi 所属类型'].append(CurPol['pois'][j]['children']['subtype'])
                    except:
                        ResList['子 poi 所属类型'].append('')
                    try:
                        ResList['子 poi 分类编码'].append(CurPol['pois'][j]['children']['typecode'])
                    except:
                        ResList['子 poi 分类编码'].append('')
                    try:
                        ResList['poi 所属商圈'].append(CurPol['pois'][j]['business']['business_area'])
                    except:
                        ResList['poi 所属商圈'].append('')
                    try:
                        ResList['poi 的联系电话'].append(CurPol['pois'][j]['business']['tel'])
                    except:
                        ResList['poi 的联系电话'].append('')
                    try:
                        ResList['poi 特色内容'].append(CurPol['pois'][j]['business']['tag'])
                    except:
                        ResList['poi 特色内容'].append('')
                    try:
                        ResList['poi 评分'].append(CurPol['pois'][j]['business']['rating'])
                    except:
                        ResList['poi 评分'].append('')
                    try:
                        ResList['poi 人均消费'].append(CurPol['pois'][j]['business']['cost'])
                    except:
                        ResList['poi 人均消费'].append('')
                    try:
                        ResList['停车场类型'].append(CurPol['pois'][j]['business']['parking_type'])
                    except:
                        ResList['停车场类型'].append('')
                    try:
                        ResList['poi 的别名'].append(CurPol['pois'][j]['business']['alias'])
                    except:
                        ResList['poi 的别名'].append('')
                    try:
                        ResList['poi 对应的导航引导点坐标'].append(CurPol['pois'][j]['navi']['navi_poiid'])
                    except:
                        ResList['poi 对应的导航引导点坐标'].append('')
                    try:
                        ResList['poi 的入口经纬度坐标'].append(CurPol['pois'][j]['navi']['entr_location'])
                    except:
                        ResList['poi 的入口经纬度坐标'].append('')
                    try:
                        ResList['poi 的出口经纬度坐标'].append(CurPol['pois'][j]['navi']['exit_location'])
                    except:
                        ResList['poi 的出口经纬度坐标'].append('')
                    try:
                        ResList['poi 的地理格 id'].append(CurPol['pois'][j]['navi']['gridcode'])
                    except:
                        ResList['poi 的地理格 id'].append('')
                    try:
                        ResList['poi 的图片介绍'].append(CurPol['pois'][j]['photos'][0]['title'])
                    except:
                        ResList['poi 的图片介绍'].append('')
                    try:
                        ResList['poi 图片的下载链接'].append(CurPol['pois'][j]['photos'][0]['url'])
                    except:
                        ResList['poi 图片的下载链接'].append('')
                    try:
                        ResList['是否有室内地图标志'].append(CurPol['pois'][j]['indoor']['indoor_map'])
                    except:
                        ResList['是否有室内地图标志'].append('')
                    try:
                        ResList['所在建筑物的 POI ID'].append(CurPol['pois'][j]['indoor']['cpid'])
                    except:
                        ResList['所在建筑物的 POI ID'].append('')
                    try:
                        ResList['楼层索引'].append(CurPol['pois'][j]['indoor']['floor'])
                    except:
                        ResList['楼层索引'].append('')
                    try:
                        ResList['所在楼层'].append(CurPol['pois'][j]['indoor']['truefloor'])
                    except:
                        ResList['所在楼层'].append('')
                ResPolList.append(CurPolList[i])
                yuanshi = pd.concat([yuanshi, pd.DataFrame(CurPol)], ignore_index=True)
            len1 = len(CurPolList)
            print('当前在查询第', i + 1, '个矩形', '队列总数', len1, CurPolList[i])
            i = i + 1
            time.sleep(0.3)
        res1 = pd.DataFrame(ResPolList)
        res2 = pd.DataFrame(ResList)
        print(res2)
        res2.to_excel('按shp查询POI_详细信息.xlsx', sheet_name='全部', index=False)
        yuanshi.to_excel('按shp查询POI_详细信息_原始获取.xlsx', sheet_name='全部', index=False)
        print('输出结果已生成在程序根目录下的“按shp查询POI_详细信息.xlsx”文件\n原始获取数据已生成在程序根目录下的“按shp查询POI_详细信息_原始获取.xlsx”文件')
    else:
        ResList = {'名称': [], '坐标': [], 'POI类型': [], '详细地址': [], '城市': [], '区县': []}
        while i < len1:
            ax = CurPolList[i][0]
            ay = CurPolList[i][1]
            bx = CurPolList[i][2]
            by = CurPolList[i][3]
            CurPol = Judge0(key, ax, ay, bx, by,guanjianci,leixing)
            if str(type(CurPol)) == "<class 'int'>":
                CurPolList.append([ax, ay, round((ax + bx) / 2, 6), round((ay + by) / 2, 6)])
                CurPolList.append([round((ax + bx) / 2, 6), ay, bx, round((ay + by) / 2, 6)])
                CurPolList.append([ax, round((ay + by) / 2, 6), round((ax + bx) / 2, 6), by])
                CurPolList.append([round((ax + bx) / 2, 6), round((ay + by) / 2, 6), bx, by])
            else:
                for j in range(0, len(CurPol['pois'])):
                    ResList['名称'].append(CurPol['pois'][j]['name'])
                    ResList['坐标'].append(CurPol['pois'][j]['location'])
                    ResList['POI类型'].append(CurPol['pois'][j]['type'])
                    ResList['详细地址'].append(CurPol['pois'][j]['address'])
                    ResList['城市'].append(CurPol['pois'][j]['cityname'])
                    ResList['区县'].append(CurPol['pois'][j]['adname'])
                ResPolList.append(CurPolList[i])
                yuanshi = pd.concat([yuanshi, pd.DataFrame(CurPol)], ignore_index=True)
            len1 = len(CurPolList)
            print('当前在查询第', i+1, '个矩形', '队列总数', len1, CurPolList[i])
            i = i + 1
            time.sleep(0.3)
        res1 = pd.DataFrame(ResPolList)
        res2 = pd.DataFrame(ResList)
        print(res2)
        res2.to_excel('按shp查询POI_简要信息.xlsx', sheet_name='全部', index=False)
        yuanshi.to_excel('按shp查询POI_详细信息_原始获取.xlsx', sheet_name='全部', index=False)
        print('输出结果已生成在程序根目录下的“按shp查询POI_简要信息.xlsx”文件\n原始获取数据已生成在程序根目录下的“按shp查询POI_简要信息_原始获取.xlsx”文件')
input('程序运行结束，按回车退出')