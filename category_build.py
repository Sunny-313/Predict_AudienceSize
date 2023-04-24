# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:21:41 2023

@author: Sunny_Yaoyao
"""


import pandas as pd
import json
import os

def load_json(file):
    if not os.path.isfile(file):
        data = {}
    else:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    return data

def build_dataframe(node, level=1):
    row = {'categoryCode': node['categoryCode'], 'name': node['name']}
    
    if 'children' in node:
        dfs = [build_dataframe(child, level=level+1) for child in node['children']]
        df = pd.concat(dfs, ignore_index=True)
        df['categoryCode'] = node['categoryCode']
        df['name'] = node['name']
    else:
        df = pd.DataFrame(row, index=[0])
    
    df = df.rename(columns={'name': f'name_{level}', 
                            'categoryCode': f'categoryCode_{level}'})
    return df


if __name__ == '__main__':
    json_path = os.path.join(os.getcwd(),'relatedCategory',"relatedCategoryList.json")
    data = load_json(json_path)
    
    li = []
    for el in data['result']:
        li.append(build_dataframe(el))
    
    df = pd.concat(li)