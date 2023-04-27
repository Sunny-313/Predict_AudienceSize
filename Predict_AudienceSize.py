# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:34:28 2023

@author: Sunny_Yaoyao
"""
import pandas as pd
import requests
import json
import os
import re
import random
import time
import warnings

warnings.filterwarnings('ignore')


def load_json(file):
    if not os.path.isfile(file):
        data = {}
    else:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    return data

def parse_cookies(cookies_file):    
    cookies = {}
    
    f = open(cookies_file, 'r')
    for line in f:
        if not re.match(r'^#|\n', line):
            line_fields = line.strip().split('\t')
            cookies[line_fields[5]] = line_fields[6]
    f.close()
    
    return cookies  

'''浏览行为_品牌/类目'''
def get_view_data(brand_id, cate_id, start_time, end_time, frequency, price):

    data = {
            "cardType": "view",
            "cardCode": "300658",
            "type": "behaviorV2",
            "key": "view",
            "screen": "all",
            "dimension": "3" if pd.isnull(brand_id) else ("1" if pd.isnull(cate_id) else"2"),
            "brandCode": '' if pd.isnull(brand_id) else str(brand_id),
            "cateList": str(cate_id) if pd.isnull(brand_id) else ("" if pd.isnull(cate_id) else str(cate_id.split("_")[-1])),
            "isRelativeTime": 'false',
            "startDate": str(start_time).rstrip("00:00:00").rstrip(),
            "endDate": str(end_time).rstrip("00:00:00").rstrip(),
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "price": {"operator": "nolimit"} if pd.isnull(price) else {"operator": "dealBetween", "value": price},
            "displayDef": "1"
                }
    return data

'''浏览行为_店铺'''
def get_view_shop_data(shop_id,start_time, end_time, frequency, price):

    data = {
            "cardType": "view",
            "cardCode": "300658",
            "type": "behaviorV2",
            "key": "view",
            "screen": "all",
            "dimension": "4",
            "shopCode": shop_id,
            "isRelativeTime": 'false',
            "startDate": str(start_time).rstrip("00:00:00").rstrip(),
            "endDate": str(end_time).rstrip("00:00:00").rstrip(),
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "price": {"operator": "nolimit"} if pd.isnull(price) else {"operator": "dealBetween", "value": price},
            "displayDef": "1"
            }
    return data


'''购买行为_品牌/类目'''
def get_order_data(brand_id, cate_id, start_time, end_time, frequency, price):

    data = {
            "cardType": "order",
            "cardCode": "300662",
            "type": "behaviorV2",
            "key": "order",
            "screen": "all",
            "dimension": "3" if pd.isnull(brand_id) else ("1" if pd.isnull(cate_id) else"2"),
            "brandCode": '' if pd.isnull(brand_id) else str(brand_id),
            "cateList": str(cate_id) if pd.isnull(brand_id) else ("" if pd.isnull(cate_id) else str(cate_id.split("_")[-1])),
            "isRelativeTime": 'false',
            "startDate": str(start_time).rstrip("00:00:00").rstrip(),
            "endDate": str(end_time).rstrip("00:00:00").rstrip(),
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "price": {"operator": "nolimit"} if pd.isnull(price) else {"operator": "dealBetween", "value": price},
            "displayDef": "1"
            }
    return data

'''购买行为_店铺'''
def get_order_shop_data(shop_id,start_time, end_time, frequency, price):

    data = {
            "cardType": "order",
            "cardCode": "300662",
            "type": "behaviorV2",
            "key": "order",
            "screen": "all",
            "dimension": "4",
            "shopCode": shop_id,
            "isRelativeTime": 'false',
            "startDate": str(start_time).rstrip("00:00:00").rstrip(),
            "endDate": str(end_time).rstrip("00:00:00").rstrip(),
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "price": {"operator": "nolimit"} if pd.isnull(price) else {"operator": "dealBetween", "value": price},
            "displayDef": "1"
            }
    return data

'''购买行为_关键词x三级类目'''
def get_order_keycate_data(shop_id,cate_id,keyWords,start_time, end_time, frequency, price):

    data = {
            "cardType": "order",
            "cardCode": "300662",
            "type": "behaviorV2",
            "key": "order",
            "screen": "all",
            "dimension": "7",
            "keyWord": keyWords,
            "cateList":str(cate_id.split("_")[-1]),
            "isRelativeTime": 'false',
            "startDate": str(start_time).rstrip("00:00:00").rstrip(),
            "endDate": str(end_time).rstrip("00:00:00").rstrip(),
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "price": {"operator": "nolimit"} if pd.isnull(price) else {"operator": "dealBetween", "value": price},
            "displayDef": "1"
            }
    return data

'''购买行为_SKU'''
def get_order_sku_data(sku_list,start_time, end_time, frequency, price):
    
    data = {
            "cardType": "order",
            "cardCode": "300662",
            "type": "behaviorV2",
            "key": "order",
            "screen": "all",
            "dimension": "5",
            "skuCode": sku_list,
            "isRelativeTime": 'false',
            "startDate": str(start_time).rstrip("00:00:00").rstrip(),
            "endDate": str(end_time).rstrip("00:00:00").rstrip(),
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "price": {"operator": "nolimit"} if pd.isnull(price) else {"operator": "dealBetween", "value": price},
            "displayDef": "1"
            }
    return data

'''获取最新已有人群ID'''
def get_old_id(cookies):

    headers = {
        'authority': '4a.jd.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'cookie': '__jdv=224457823|direct|-|none|-|1681901189175; __jdu=1681901189175424004703; jd.dm.lang=zh_CN; logining=1; dm_profile=false; 3AB9D23F7A4B3C9B=LDBURB5Y2AYR6D53KUXJ4WSUI5CJJ2HV74URP3IT333QC2L32HQ3U36RK2EPP22GGVZ44TQ254N4Y2LIWCQAJMGGXI; wlfstk_smdl=kri9aruvrt1knrzubn86gr1pcn8m7txr; TrackID=1ua9FD9N81h2kZN45TPK7Fj8L5fjrx6l966P60a2BxZZ80O39zZrnBTDAqZLTxJLgks73LLs1_z7K4lKRpraVMqPMI4bxhtTqzhdYaD5dSDM; thor=D896B980507952992416A2E7D770B5E5BF7D3FAC48AB92B01D9E4DE82A6E4ADA33FE2022B1F6C9D389FF0A062374B45B7E9BA697E32F3678B94385AE5422BFBDE82A2B9ADBEB141B469755DEBF5762D5993AA60081786F66AD7C8F84F460AD4566E20EF2335ECAA19E78CE3FC632F6EDD5B716229DAAF909AC4D085916DD2005; pinId=h0gvEoXeuRLeecPYgj8c8A; pin=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE; unick=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE; ceshi3.com=203; _tp=lVgPTDCL%2FyWF%2FoLJhRna9Vmoaw2x6voQZQELfasIUTj6Fy6C1udLA4PP0Aji8T3%2F; _pst=%E4%BD%B3%E6%B2%9B%E6%B3%BD%E6%99%AE; passport_pin=5L2z5rKb5rO95pmu; pin_account=5L2z5rKb5rO95pmu; press_pin=5L2z5rKb5rO95pmu; __jda=224457823.1681901189175424004703.1681901189.1682319187.1682321492.14; __jdc=224457823; __jdb=224457823.15.1681901189175424004703|14.1682321492',
        'referer': 'https://4a.jd.com/datamill/growthStrategy/audienceManagement.html',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sgm-context': '157150137813415140;157150137813415140',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'uuid': 'undefined',
    }
    
    params = {
        'name': '',
        'startDate': '2021-04-24',
        'endDate': '2023-04-24',
        'status': '-1',
        'audienceType': 'all',
        'pageNum': '0',
        'pageSize': '100',
    }
    
    try:
        url = "https://4a.jd.com/datamill/api/growthStrategy/audienceManagement/audienceList"
        response = requests.get(
            url = url,
            params=params,
            cookies=cookies,
            headers=headers,
        )
        
        id_list = json.loads(response.content.decode())
    
    except Exception as e:
        print("Error: ", e)
        
    return id_list

'''已有人群'''
def get_old_data(id_list,name):      

    
    for info in id_list["result"]['data']:
        if info["name"] == name:
            audienceId = info["id"]
            
    data = {
        
            "cardType": "custom",
            "cardCode": "102180",
            "categoryPath": "已有人群",
            "type": "package",
            "audienceId": audienceId,
            'originCardType': 'audience',
            'cardTitle': '已有人群'

        }
    return data

'''获取广告ID'''
def get_ad_id(cookies, ad_name):
    name_list = ad_name.split(",")
    ad_id = ''
    url = 'https://4a.jd.com/datamill/api/audienceManagement/newCustomAudienceEditInner/lineList'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }
    txt = requests.get(url=url,cookies=cookies,headers=headers).text
    data_list = json.loads(txt)["result"]["data"]
    for data in data_list:
        if data["name"] in name_list:
            ad_id += str(data["id"])
            ad_id += ','
    return ad_id.rstrip(",")

'''广告行为'''
def get_ad_data(cookies,brand_id,cate_id, ad_name, behavior, start_time, end_time, frequency):
    ad_id = get_ad_id(cookies, ad_name)
    data = {
            "cardType": "advertisement",
            "cardTitle": "广告行为",
            "cardCode": "300270",
            "key": "impression" if behavior == '曝光' else "click",
            "type": "behaviorV2",
            "line": str(ad_id),
            "behaviorType": "impression" if behavior == '曝光' else "click",
            "isRelativeTime": 'false',
            "frequency": {"operator": "nolimit"} if pd.isnull(frequency) else {"operator": "between", "value": frequency},
            "dimension": "1" if pd.isnull(cate_id) else "2",
            "startDate": str(start_time).rstrip("00:00:00").rstrip(),
            "endDate": str(end_time).rstrip("00:00:00").rstrip(),
            "brandCode": brand_id,
            "cateList": "" if pd.isnull(cate_id) else str(cate_id.split("_")[-1]),
            "displayDef": "1"
             }
    return data


'''搭建逻辑'''
def get_data(cookies,df):
    for index, row in df.iterrows():
        if row["卡片名称"] == "浏览行为_品牌/类目":
            data = get_view_data(row['Key_ID'], row['类目ID'], row['开始时间'], row['结束时间'], row['频次'], row['价格'])    
        if row["卡片名称"] == "浏览行为_店铺":
            data = get_view_data(row['Key_ID'], row['开始时间'], row['结束时间'], row['频次'], row['价格'])
        elif row["卡片名称"] == "购买行为_品牌/类目":
            data = get_order_data(row['Key_ID'], row['类目ID'], row['开始时间'], row['结束时间'], row['频次'], row['价格'])
        elif row["卡片名称"] == "购买行为_店铺":
            data = get_order_shop_data(row['Key_ID'], row['开始时间'], row['结束时间'], row['频次'], row['价格'])
        elif row["卡片名称"] == "购买行为_关键词x三级类目":
            data = get_order_keycate_data(row['Key_ID'], row['类目ID'],row['KeyWords'],row['开始时间'], row['结束时间'], row['频次'], row['价格'])
        elif row["卡片名称"] == "购买行为_SKU":           
            data = get_order_sku_data(row['sku_list'],row['开始时间'], row['结束时间'], row['频次'], row['价格'])
        elif row["卡片名称"] == "已有人群":           
            data = get_old_data(id_list, row['已有人群'])
        elif row["卡片名称"] == "广告行为":           
            data = get_ad_data(cookies,row['Key_ID'], row['类目ID'],row['渠道'],row['行为'],row['开始时间'], row['结束时间'], row['频次'])
    return data


'''读取逻辑,返回人群名与data'''
def get_card(path): 
    card_list = []
    df = pd.read_excel(path, dtype={'Key_ID': 'str'})
    people_list = df['人群名称'].drop_duplicates() 
    for people in people_list:
        df1 = df[df["人群名称"] == people]
        df1 = df1.reset_index(drop=True)
        '''单人群标签'''
        if len(df1) == 1: 
            data = eval('{"audienceDefinition":{"type":"intersection","children":[' + str(get_data(cookies,df1)) + ']}}')
        else:
            data2 = str(get_data(cookies,df1.loc[[0]]))
            for i in range(len(df1)-1):
                if df1.iloc[i+1, 1] == "交集":
                    operation = "intersection"
                elif df1.iloc[i+1, 1] == "差集":
                    operation = "diff"
                elif df1.iloc[i+1, 1] == "并集":
                    operation = "union"
                data2 = '{"type":"' + operation + '","children":[' + data2 + ',' + str(get_data(cookies,df1.loc[[i+1]])) + ']}'
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
    try:
        r = requests.post(url=url, cookies=cookies,headers=headers, json=info)  
    except Exception as e:
        print("Error: ", e)
        
    return r.text

if __name__ == '__main__':
    cookies_file = os.path.join(os.path.dirname('__file__'), 'cookies.txt')
    cookies = parse_cookies(cookies_file)
    
    # 获取最新已有人群ID
    id_list = get_old_id(cookies)

    result_list = []
    path = os.path.join(os.getcwd(),'ruleSheet','data_sheet.xlsx')
    people_list = get_card(path=path)
    for people in people_list:
        people_size = eval(people_count(cookies, people["data"]))
        result_list.append(
            {
                "人群名称" : people["name"],
                "人群大小" : people_size["result"]["audienceSize"]
            }
        )
        
        '''设置一个延迟时长 '''
        delay = random.randint(10000,50000)/10000
        print('延迟时长 %f s' % delay)
        print('人群包: {}大小为：{}'.format(people["name"],people_size["result"]["audienceSize"]))
        print("-------------------------------------------------------")
        time.sleep(delay) 
        
    result_df = pd.DataFrame(result_list)
    result_df.to_excel('result.xlsx', index=None, header=True)
