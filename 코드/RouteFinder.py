# -*- coding: utf-8 -*-
# Currently, this code is for API which return JSON type
# TODO : Change JSON type to XML / Save DB at another path


import requests
import sqlite3
from xml.etree.ElementTree import parse
from pandas import Series, DataFrame

def requestData() :
    APP_KEY = 'g%2F5KztLAmoWSiTeIdbG0jZXlwG4YGfheb0P7zQzKoxZBapGCIMWPIkMuQRQ9nB1YXMmFBXJi6fKxBJshDQmxZA%3D%3D'
    Operation = 'getCtyCodeList'
    ret = DataFrame()
    hosturl = 'http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/getCtyCodeList'
    hosturl = hosturl + Operation + '?ServiceKey=' + APP_KEY
    myResponse = requests.get(hosturl)
    if(myResponse.ok):
        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)        ret = DataFrame(jData)
        tree = parse(myResponse)
        note = tree.getroot()
        print(ret)

        #ret = ret.append(output, ignore_index = True)
    else:
        # If response code is not ok (200), print the resulting http error code with description
            myResponse.raise_for_status()
    return ret

source = requestData()
# SQLite DB 연결
conn = sqlite3.connect("test.db")
# Connection 으로부터 Cursor 생성
cur = conn.cursor()
source.to_sql("station", conn)
# Connection 닫기
conn.close()
