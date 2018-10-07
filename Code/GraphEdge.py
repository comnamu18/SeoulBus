# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import urllib
import requests

import XML2DataFrame as xdf

class GraphEdge:
    rawData = None
    busType = 1
    busList = pd.Series()

    def __init__(self, fileName, busType):
        self.rawData = pd.read_csv(fileName)
        self.busType =  busType
        self.busList = pd.Series(self.rawData['노선번호'])
    def createEdge(self) :
        #setting return type
        ret = list()

        #default REST url settings
        APP_KEY = 'ServiceKey=V4zKer6ld4jMtoMBafRG9Zf4XU1zr%2FyiEWoWxv9UcUQOvvSTc1Rd13hM2%2Faax1GyqCA6AMg9H6pOkDiui4te9Q%3D%3D&'
        hosturl = 'http://ws.bus.go.kr/api/rest/busRouteInfo/'
        IDOPName = 'getBusRouteList?'
        ROUTEOPName = 'getStaionByRoute?'

        for busNm in self.busList:
            print(busNm)
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
                print(busNm + "Will be added")
                ret.append(xml2df.process_route())

        return ret
