import xml.etree.ElementTree as ET
import pandas as pd

class XML2DataFrame:
    def __init__(self, xml_data):
        self.root = ET.XML(xml_data)
        self.itemList = self.root.findall('.//itemList')
    #find BusRoute Id
    def process_id(self, busRouteNm):
        ret = None
        for item in self.itemList:
            bNm = item.find('busRouteNm').text
            if item.find('routeType').text == '2' or item.find('routeType').text == '4' or item.find('routeType').text == '3' or item.find('routeType').text == '5':
                if bNm == str(busRouteNm):
                    ret = item.find('busRouteId').text
        return ret
    #find BusStop's by tuples List
    def process_route(self):
        ret = list()
        bNm = None
        for item in self.itemList:
            sNm = item.find('arsId').text
            if bNm is not None:
                ret.append((bNm, sNm))
            bNm = sNm
        return ret
