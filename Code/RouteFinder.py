# -*- coding: utf-8 -*-

import requests
import pandas as pd
import urllib
import json

def requestData() :
    APP_KEY = 'g%2F5KztLAmoWSiTeIdbG0jZXlwG4YGfheb0P7zQzKoxZBapGCIMWPIkMuQRQ9nB1YXMmFBXJi6fKxBJshDQmxZA%3D%3D'
    OPName = 'getCtyCodeList?'
    hosturl = 'http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/'
    f = {urllib.parse.quote_plus('ServiceKey') : APP_KEY, urllib.parse.quote_plus('파라미터영문명'):'파라미터기본값'}
    hosturl = hosturl + OPName + urllib.parse.urlencode(f)
    print(hosturl)
    myResponse = requests.get(hosturl)
    ret = pd.DataFrame()
    if(myResponse.ok):
        jData = json.loads(myResponse.content)
        print(jData)
    else:
        print("WRONG!")
        myResponse.raise_for_status()

    return ret

requestData()