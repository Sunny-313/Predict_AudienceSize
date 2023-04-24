# -*- coding: utf-8 -*-
"""
Created on Thu May 26 14:47:29 2022

@author: Sunny_Yaoyao
"""
import pandas as pd
import requests
import json
import os
import re

def parse_cookies(cookies_file):    
    cookies = {}
    
    f = open(cookies_file, 'r')
    for line in f:
        if not re.match(r'^#|\n', line):
            line_fields = line.strip().split('\t')
            cookies[line_fields[5]] = line_fields[6]
    f.close()
    
    return cookies  

def make_path(*dirs):
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(root, *dirs)

def is_file(file):
    if os.path.isfile(file):
        print('File is already existed: %s' % file)
        return True
    return False

def get_core_id(cookies, cate_name): # 拿品牌三级类目id

    cate1 = list(cate_name.split('-'))[0]
    cate2 = list(cate_name.split('-'))[1]
    cate3 = list(cate_name.split('-'))[2]
    
    url = 'https://4a.jd.com/datamill/api/accountManagement/mainAccountInfoOuter/brandInfo'
    headers = {
    'authority': '4a.jd.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookies': '__jdv=224457823|direct|-|none|-|1681901189175; __jdu=1681901189175424004703; jd.dm.lang=zh_CN; logining=1; 3AB9D23F7A4B3C9B=LDBURB5Y2AYR6D53KUXJ4WSUI5CJJ2HV74URP3IT333QC2L32HQ3U36RK2EPP22GGVZ44TQ254N4Y2LIWCQAJMGGXI; wlfstk_smdl=8hz4ndx01j15gy1ukyt6ebl5spoqj1or; TrackID=1gKavk6fWlVc1RCvUnikqQ9yzrnUNT3Lf4n4k377ridiEJFQHYAXr9yNuTKBHLjoV0sEPz8W8l1dVdFX6qwz_nlo8sJOcRdtbZfw5uoUOMgs; thor=77929045D8166F46D57D80E74D08E9DAEAE3520824E81EDB40E6A573E52BB2AE5E0CFFAA0206F04761952B31C7EE75607D494231C352D1A21639DFF5573CA3637B4088D4F13AA3B6EAA80F29A0328713ADC3C118E9CF84B1A56BCDB7641EBABB27C8718B91C82F449D53E93F0EE059FD5A176673EC3AB3B1A3999A91C22C52CB; pinId=h0gvEoXeuRKtxuNuqj_g-R0n2gfmNTW7; pin=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE%E6%B0%B4%E6%9E%9C; unick=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE%E6%B0%B4%E6%9E%9C; ceshi3.com=000; _tp=lVgPTDCL%2FyWF%2FoLJhRna9Vmoaw2x6voQZQELfasIUTgTkB%2F5wQM4PctaKaBvdSvWVelAafqMltjDwiqTQtlmUQ%3D%3D; _pst=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE%E6%B0%B4%E6%9E%9C; passport_pin=5L2z5rKb5rO95pmu5rC05p6c; pin_account=5L2z5rKb5rO95pmu5rC05p6c; press_pin=5L2z5rKb5rO95pmu5rC05p6c; __jda=224457823.1681901189175424004703.1681901189.1682054343.1682057660.5; __jdc=224457823; dm_profile=false; __jdb=224457823.15.1681901189175424004703|5.1682057660',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    
    }
    
    txt = requests.get(url,cookies=cookies,headers=headers).text
    data = json.loads(txt)["result"]["data"][0]
    brand_id = data['brandCode']
    cate_list = data["category"]

    for i in range(30):
        if cate_list[i]["name"] == cate1:
            cate_id1 = cate_list[i]["categoryCode"]
            cate_children = cate_list[i]["children"]
            break

    for j in range(30):
        if cate_children[j]["name"] == cate2:
            cate_id2 = cate_children[j]["categoryCode"]
            cate_grandson = cate_children[j]["children"]
            break

    for k in range(30):
        if cate_grandson[k]["name"] == cate3:
            cate_id3 = cate_grandson[k]["categoryCode"]
            break

    cate_id = str(cate_id1) + "_" + str(cate_id2) + "_" + str(cate_id3)
    id_data = {
        "brand_id": brand_id,
        "cate_id": cate_id
    }
    
    return id_data

'''浏览行为'''
def get_view_data(cookies, brand_name, cate_name, start_time, end_time, frequency, price):
    brand_id = get_core_id(cookies, cate_name)["brand_id"]
    cate_id = get_core_id(cookies, cate_name)["cate_id"]
    data = {
            "cardType": "view",
            "cardCode": "300658",
            "type": "behaviorV2",
            "key": "view",
            "screen": "all",
            "dimension": "3" if pd.isnull(brand_name) else "2",
            "brandCode": '' if pd.isnull(brand_name) else str(brand_id),
            "cateList": str(cate_id) if pd.isnull(brand_name) else str(cate_id.split("_")[-1]),
            "isRelativeTime": 'false',
            "startDate": str(start_time).rstrip("00:00:00").rstrip(),
            "endDate": str(end_time).rstrip("00:00:00").rstrip(),
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "price": {"operator": "nolimit"} if pd.isnull(price) else {"operator": "between", "value": price},
            "displayDef": "1"
                }
    return data


'''购买行为'''
def get_order_data(cookies, brand_name, cate_name, start_time, end_time, frequency, price):
    brand_id = get_core_id(cookies, cate_name)["brand_id"]
    cate_id = get_core_id(cookies, cate_name)["cate_id"]
    data = {
            "cardType": "order",
            "cardCode": "300662",
            "type": "behaviorV2",
            "key": "order",
            "screen": "all",
            "dimension": "3" if pd.isnull(brand_name) else "2",
            "brandCode": '' if pd.isnull(brand_name) else str(brand_id),
            "cateList": str(cate_id) if pd.isnull(brand_name) else str(cate_id.split("_")[-1]),
            "isRelativeTime": 'false',
            "startDate": str(start_time).rstrip("00:00:00").rstrip(),
            "endDate": str(end_time).rstrip("00:00:00").rstrip(),
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "price": {"operator": "nolimit"} if pd.isnull(price) else {"operator": "between", "value": price},
            "displayDef": "1"
            }
    return data

def get_addCart_data(cookie, brand_name, cate_name, start_time, end_time, frequency, price): 
    brand_id = get_core_id(cookie, cate_name)["brand_id"]
    cate_id = get_core_id(cookie, cate_name)["cate_id"]
    data = {
            "cardType": "addCart",
            "cardCode": "300666",
            "type": "behaviorV2",
            "key": "addCart",
            "screen": "all",
            "dimension": "3" if pd.isnull(brand_name) else "2",
            "brandCode": '' if pd.isnull(brand_name) else str(brand_id),
            "cateList": str(cate_id) if pd.isnull(brand_name) else str(cate_id.split("_")[-1]),
            "isRelativeTime": 'false',
            "startDate": start_time,
            "endDate": end_time,
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "price": {"operator": "nolimit"} if pd.isnull(price) else {"operator": "between", "value": price},
            "displayDef": "1"  
            }
    return data

'''广告行为'''
def get_ad_id(cookie, ad_name): # 拿广告id
    name_list = ad_name.split(",")
    ad_id = ''
    url = 'https://4a.jd.com/datamill/api/audienceManagement/newCustomAudienceEditInner/lineList'
    headers = {
    'authority': '4a.jd.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookies': '__jdv=224457823|direct|-|none|-|1681901189175; __jdu=1681901189175424004703; jd.dm.lang=zh_CN; logining=1; 3AB9D23F7A4B3C9B=LDBURB5Y2AYR6D53KUXJ4WSUI5CJJ2HV74URP3IT333QC2L32HQ3U36RK2EPP22GGVZ44TQ254N4Y2LIWCQAJMGGXI; wlfstk_smdl=8hz4ndx01j15gy1ukyt6ebl5spoqj1or; TrackID=1gKavk6fWlVc1RCvUnikqQ9yzrnUNT3Lf4n4k377ridiEJFQHYAXr9yNuTKBHLjoV0sEPz8W8l1dVdFX6qwz_nlo8sJOcRdtbZfw5uoUOMgs; thor=77929045D8166F46D57D80E74D08E9DAEAE3520824E81EDB40E6A573E52BB2AE5E0CFFAA0206F04761952B31C7EE75607D494231C352D1A21639DFF5573CA3637B4088D4F13AA3B6EAA80F29A0328713ADC3C118E9CF84B1A56BCDB7641EBABB27C8718B91C82F449D53E93F0EE059FD5A176673EC3AB3B1A3999A91C22C52CB; pinId=h0gvEoXeuRKtxuNuqj_g-R0n2gfmNTW7; pin=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE%E6%B0%B4%E6%9E%9C; unick=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE%E6%B0%B4%E6%9E%9C; ceshi3.com=000; _tp=lVgPTDCL%2FyWF%2FoLJhRna9Vmoaw2x6voQZQELfasIUTgTkB%2F5wQM4PctaKaBvdSvWVelAafqMltjDwiqTQtlmUQ%3D%3D; _pst=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE%E6%B0%B4%E6%9E%9C; passport_pin=5L2z5rKb5rO95pmu5rC05p6c; pin_account=5L2z5rKb5rO95pmu5rC05p6c; press_pin=5L2z5rKb5rO95pmu5rC05p6c; __jda=224457823.1681901189175424004703.1681901189.1682054343.1682057660.5; __jdc=224457823; dm_profile=false; __jdb=224457823.15.1681901189175424004703|5.1682057660',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    txt = requests.get(url=url,cookies=cookies,headers=headers).text
    data_list = json.loads(txt)["result"]["data"]
    for data in data_list:
        if data["name"] in name_list:
            ad_id += str(data["id"])
            ad_id += ','
    return ad_id.rstrip(",")

def get_ad_data(cookie, brand_name, cate_name, ad_name, behavior, start_time, end_time, frequency):  # 广告行为
    brand_id = get_core_id(cookie, cate_name)["brand_id"]
    cate_id = get_core_id(cookie, cate_name)["cate_id"]
    ad_id = get_ad_id(cookie, ad_name)
    data = {
            "cardType": "advertisement",
            "cardTitle": "广告行为",
            "cardCode": "300270",
            "key": "impression",
            "type": "behaviorV2",
            "line": str(ad_id),
            "behaviorType": "impression" if behavior == '曝光' else "click",
            "isRelativeTime": 'false',
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "dimension": "10" if brand_id == '' else "2" ,#10指三级类目、1指品牌维度、2指品牌x三级类目
            "startDate": start_time,
            "endDate": end_time,
            "brandCode": brand_id,
            "cateList": cate_id,
            "displayDef": "1"
             }
    return data



'''4A分布（待完善）'''
def get_4a_data(cookie, brand_name, cate_name, start_time, end_time, status):
    brand_id = get_core_id(cookie, cate_name)["brand_id"]
    cate_id = get_core_id(cookie, cate_name)["cate_id"]
    status_list = status.split(",")
    if "认知" in status_list:
        pass
    data = {
        "audienceDefinition": {
            "type": "intersection",
            "children": [
                {
                    "cardType": "layout",
                    "cardTitle": "4A分布",
                    "cardCode": "300214",
                    "type": "4alayoutV2",
                    "modelType": "1",
                    "brandCode": str(brand_id),
                    "cateList": str(cate_id) if pd.isnull(brand_name) else str(cate_id.split("_")[-1]),
                    "status": status,
                    "isRelativeTime": "false",
                    "startDate": start_time,
                    "endDate": end_time,
                    "displayDef": "1"
                }
            ]
        }
    }
    return data

def get_data(cookies,df):
    for index, row in df.iterrows():
        if row["卡片名称"] == "浏览行为":
            data = get_view_data(cookies, row['品牌'], row['类目'], row['开始时间'], row['结束时间'], row['频次'], row['价格'])    
        elif row["卡片名称"] == "购买行为":
            data = get_order_data(cookies, row['品牌'], row['类目'], row['开始时间'], row['结束时间'], row['频次'], row['价格'])
        elif row["卡片名称"] == "加购行为":
            data = get_addCart_data(cookies, row['品牌'], row['类目'], row['开始时间'], row['结束时间'], row['频次'], row['价格'])   
        elif row["卡片名称"] == "广告行为":
            data = get_ad_data(cookies, row['品牌'], row['类目'], row['渠道'], row['行为'], row['开始时间'], row['结束时间'], row['频次'])
    return data

def get_card(cookies, path): # 读取逻辑,返回人群名与data
    card_list = []
    df = pd.read_excel(path)
    people_list = df['人群名称'].drop_duplicates() # 提取人群名称列后去重，拿到全部人群名称
    for people in people_list:
        df1 = df[df["人群名称"].str.contains(people)]
        df1 = df1.reset_index(drop=True)
        if len(df1) == 1: # 如果人群只有一个卡片
            data = eval('{"audienceDefinition":{"type":"intersection","children":[' + str(get_data(cookies, df1)) + ']}}')
        else: # 多个卡片
            data2 = str(get_data(cookies, df1.loc[[0]]))
            for i in range(len(df1)-1):
                if df1.iloc[i+1, 1] == "交集":
                    operation = "intersection"
                elif df1.iloc[i+1, 1] == "差集":
                    operation = "diff"
                elif df1.iloc[i+1, 1] == "并集":
                    operation = "union"
                data2 = '{"type":"' + operation + '","children":[' + data2 + ',' + str(get_data(cookies, df1.loc[[i+1]])) + ']}'
            data_fall = '{"audienceDefinition":' + data2 + '}'
            data = eval(data_fall)
        card_data = {
            "name" : people,
            "data" : data
        }
        card_list.append(card_data)
    return card_list

def people_count(cookies, info):
    url = 'https://4a.jd.com/datamill/api/audienceManagement/predictAudienceSize'
    headers = {
        'authority': '4a.jd.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/json;charset=UTF-8',
        # 'cookie': '__jdv=224457823|direct|-|none|-|1681901189175; __jdu=1681901189175424004703; jd.dm.lang=zh_CN; pinId=h0gvEoXeuRKtxuNuqj_g-R0n2gfmNTW7; pin=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE%E6%B0%B4%E6%9E%9C; unick=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE%E6%B0%B4%E6%9E%9C; _tp=lVgPTDCL%2FyWF%2FoLJhRna9Vmoaw2x6voQZQELfasIUTgTkB%2F5wQM4PctaKaBvdSvWVelAafqMltjDwiqTQtlmUQ%3D%3D; _pst=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE%E6%B0%B4%E6%9E%9C; wlfstk_smdl=ruwa0yytgywrtroy8uflemnhuhmu7p2y; 3AB9D23F7A4B3C9B=LDBURB5Y2AYR6D53KUXJ4WSUI5CJJ2HV74URP3IT333QC2L32HQ3U36RK2EPP22GGVZ44TQ254N4Y2LIWCQAJMGGXI; TrackID=1Nqo_leIP1y50wCm2XNgAVQA20OJV4mXSLYyXcqwWHBA56NHEH4LG8DU02hklohRyixmd5B56-whebiCZTvknmrdvnzlLX8aD0-8bUbI5eIU; thor=77929045D8166F46D57D80E74D08E9DAC6B26C60A87CDBEE6146B742F3FF5EB1FFF1C9E0A99D6C0589371BCD25093EDE9B93A26191479294CEF8CEF6C71AA493F73877AAEF6DD433E62595BAEA47BCF3A0D2232CA7DAC30CACEF35FD0E60D39F19BE5FDBF966D095360465B5655019B03DE96369005281094214FCDE5AF651D0; ceshi3.com=000; logining=1; passport_pin=5L2z5rKb5rO95pmu5rC05p6c; pin_account=5L2z5rKb5rO95pmu5rC05p6c; press_pin=5L2z5rKb5rO95pmu5rC05p6c; __jda=224457823.1681901189175424004703.1681901189.1682057660.1682227527.6; __jdc=224457823; dm_profile=false; __jdb=224457823.17.1681901189175424004703|6.1682227527',
        'origin': 'https://4a.jd.com',
        'referer': 'https://4a.jd.com/datamill/audienceManagement/newAudienceSelectionOuter.html',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sgm-context': '484124111210403600;484124111210403600',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'uuid': 'undefined',
    }
    r = requests.post(url=url, cookies=cookies,headers=headers, json=info)
    return r.text

if __name__ == '__main__':
    cookies_file = os.path.join(os.path.dirname('__file__'), 'zespri_cookies.txt')
    cookies = parse_cookies(cookies_file)
    
    result_list = []
    path = os.path.join(os.getcwd(),'data_sheet.xlsx')
    people_list = get_card(cookies=cookies, path=path)
    for people in people_list:
        people_size = eval(people_count(cookies, people["data"]))
        result_list.append(
            {
                "人群名称" : people["name"],
                "人群大小" : people_size["result"]["audienceSize"]
            }
        )
    result_df = pd.DataFrame(result_list)
    result_df.to_excel('output/output.xlsx', index=None, header=True)
