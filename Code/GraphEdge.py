# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import urllib
import requests

import XML2DataFrame as xdf

class GraphEdge:
    rawData = None
    busType = int()
    busList = list()

    def __init__(self, fileName, busType):
        self.rawData = pd.read_csv(fileName)
        self.busType = busType
        self.busType =  busType
        self.busList = pd.Series(self.rawData['노선번호'])
    def createEdge(self) :
        #setting return type
        ret = list()

        #default REST url settings
        APP_KEY = 'serviceKey=5CQ9SA5qWhO0FwqcEFZDa%2BBreOSi1VBRXxQcGgpQQw%2FghXivHoiMgMRzzblvToQ00GoZuqIStC%2Ft0zxZiyyYlw%3D%3D&'
        hosturl = 'http://ws.bus.go.kr/api/rest/busRouteInfo/'
        IDOPName = 'getBusRouteList?'
        ROUTEOPName = 'getStaionByRoute?'

        for busNm in self.busList:
            #Get Sepcific Bus ID From API
            f = {urllib.parse.quote_plus('strSrch') : busNm}
            idHosturl = hosturl + IDOPName + APP_KEY + urllib.parse.urlencode(f)
            myResponse = requests.get(idHosturl)
            xml2df = xdf.XML2DataFrame(myResponse.content)
            busId = xml2df.process_id(busNm)
            if busId is not None:
                #Get Bus Route From API
                f = {urllib.parse.quote_plus('busRouteId') : busId}
                routeHosturl = hosturl + ROUTEOPName + APP_KEY + urllib.parse.urlencode(f)
                myResponse = requests.get(routeHosturl)
                xml2df = xdf.XML2DataFrame(myResponse.content)
                ret.append(xml2df.process_route())
            else:
                print("BUS" + str(busNm) + " is not exist in API")
        return ret
