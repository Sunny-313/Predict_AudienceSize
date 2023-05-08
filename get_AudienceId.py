# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 16:02:55 2023

@author: Sunny
"""

import requests
import os
import re
import json
import pandas as pd

def parse_cookies(cookies_file):    
    cookies = {}
    
    f = open(cookies_file, 'r')
    for line in f:
        if not re.match(r'^#|\n', line):
            line_fields = line.strip().split('\t')
            cookies[line_fields[5]] = line_fields[6]
    f.close()
    
    return cookies

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
if __name__ == '__main__':
    '''解析cookie'''
    cookies_file = os.path.join(os.path.dirname('__file__'), 'cookies.txt')
    cookies = parse_cookies(cookies_file)
    
    while True:
        li = [pd.DataFrame()]
        inputPage = int(input("请输入需要下载的已有人群包个数(50的倍数)："))
        if inputPage%50 == 0:
            pageNum = inputPage//50
            for i in range(pageNum):
                params = {
                    'name': '',
                    'startDate': '',
                    'endDate': '',
                    'status': '-1',
                    'audienceType': 'all',
                    'pageNum': str(i),
                    'pageSize': '50',
                }
                
                try:
                    url = "https://4a.jd.com/datamill/api/growthStrategy/audienceManagement/audienceList"
                    response = requests.get(
                        url = url,
                        params=params,
                        cookies=cookies,
                        headers=headers,
                    )
                    
                    res_str = json.loads(response.content.decode())
                    
                    '''解析json文件'''
                    df = pd.json_normalize(res_str['result']['data'])
                    df = df[["name","id","audienceSize"]]
                    li.append(df)
                    
                except Exception as e:
                    print("Error: ", e)
                      
            pack_list = pd.concat(li, axis=0, ignore_index=True, sort=False)
            
            break
        else:
            print("输入数字有误，请重新输入！")
            print("-------------------------------------------------------------")
            continue
    print('任务完成!请在output文件夹中查看~')
    
    pack_list.to_excel('output/audienceId.xlsx', dtype={'id': 'str'},index=None, header=True)

