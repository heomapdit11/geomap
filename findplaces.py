#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
import json
import time


def findplaces(L, N, R):
    '''Tìm 50 địa điểm N tại vị trí L trong bán kính R
    '''
    # lấy api key từ file mapapi
    with open('mapapi', 'r')  as f:
        API_KEY = f.read()
    # lấy lat và lng từ googlemap
    ses_location = requests.session()
    req_location = ses_location.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={}'.format(L, API_KEY))
    location_json = json.loads(req_location.text)
    lat = location_json['candidates'][0]['geometry']['location']['lat']
    lng = location_json['candidates'][0]['geometry']['location']['lng']
    location = '{}, {}'.format(lat, lng)
    # lấy file json từ google api
    ses = requests.session()
    req = ses.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&radius={}&language=vi&keyword={}&key={}&pagetoken='.format(location, R, N, API_KEY))
    info_json = json.loads(req.text)
    next_page_token = info_json['next_page_token']
    addr_final = ''
    n = 1
    tmp_1 = {'type': 'FeatureCollection', 'features': []}
    # xử lý api lấy tất cả thông tin của trang 1, 2 và chỉ lấy 10 vị trí tại trang 3
    for i in range(3):
        next_page_token = ''
        ses = requests.session()
        req = ses.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&radius={}&language=vi&keyword={}&key={}&pagetoken={}'.format(location, R, N, API_KEY, next_page_token))
        info_json = json.loads(req.text)
        if i == 2:
            for u in range(10):
                name_location_search = info_json['results'][u]['name']
                dict_location_search = info_json['results'][u]['plus_code']['compound_code']
                addr_location_search = info_json['results'][u]['vicinity'] + dict_location_search[7:]
                addr_final += ("{} số {} tên là: {}\nĐịa chỉ: {}\n".format(N, n, name_location_search, addr_location_search))
                tmp_3 = {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [info_json['results'][u]['geometry']['location']['lng'],info_json['results'][u]['geometry']['location']['lat']]}, 'properties': {'Address': addr_location_search, 'name': info_json['results'][u]['name']}}
                tmp_1['features'].append(tmp_3)
                n += 1
        else:
            for i in info_json['results']:
                name_location_search = i['name']
                dict_location_search = i['plus_code']['compound_code']
                addr_location_search = i['vicinity'] + dict_location_search[7:]
                addr_final += ("{} số {} tên là: {}\nĐịa chỉ: {}\n".format(N, n, name_location_search, addr_location_search))
                tmp_2 = {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [i['geometry']['location']['lng'],i['geometry']['location']['lat']]}, 'properties': {'Address': addr_location_search, 'name': i['name']}}
                tmp_1['features'].append(tmp_2)
                n += 1
        time.sleep(5)
        page_token = info_json['next_page_token']
        next_page_token += page_token
    # lưu thông tin xử lý vào file theo dạng json
    with open('mapthong.geojson', 'w', encoding='utf-8') as f:
        json.dump(tmp_1, f, ensure_ascii=False)
    return addr_final


def main():
    '''Xử lý input
    '''
    addr = input("Nhập địa chỉ tìm kiếm: ")
    search = input("Bạn muốn tìm gì từ địa chỉ trên: ")
    radius = input("Vùng tìm kiếm (m): ")
    print("Hệ thống đang tìm kiếm")
    print(findplaces(addr, search, radius))


if __name__ == "__main__":
    main()
