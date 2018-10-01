# -*- coding: utf-8 -*-

import requests
import pandas as pd
import urllib
import xml.etree.ElementTree as ET

class XML2DataFrame:

    def __init__(self, xml_data):
        self.root = ET.XML(xml_data)

    def parse_root(self, root):
        return [self.parse_element(child) for child in iter(root)]

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()
        for key in element.keys():
            if key not in parsed:
                parsed[key] = element.attrib.get(key)
            else:
                raise ValueError('duplicate attribute {0} at element {1}'.format(key, element.getroottree().getpath(element)))

        for child in list(element): 
            self.parse_element(child, parsed)

        return parsed

    def process_data(self):
        structure_data = self.parse_root(self.root)
        return pd.DataFrame(structure_data)

def requestData() :
    APP_KEY = 'g%2F5KztLAmoWSiTeIdbG0jZXlwG4YGfheb0P7zQzKoxZBapGCIMWPIkMuQRQ9nB1YXMmFBXJi6fKxBJshDQmxZA%3D%3D'
    OPName = 'getCtyCodeList?'
    hosturl = 'http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/'
    hosturl = hosturl + OPName + 'Servicekey=' + APP_KEY
    myResponse = requests.get(hosturl)
    ret = pd.DataFrame()
    if(myResponse.ok):
        print(myResponse.content)
        xml2df = XML2DataFrame(myResponse.content)
        xml_dataframe = xml2df.process_data()
        print(xml_dataframe)
    else:
        print("WRONG!")
        myResponse.raise_for_status()

    return ret

requestData()