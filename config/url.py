import unittest
import requests
import json

testheaders = {'Cookie':'insight_uid=357; laravel_session=FIBuD05nidyFgH7aRQzJfZsbM2ioFlJ9yDC4KvT7; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22357%22%2C%22%24device_id%22%3A%2216782d85fb025a-0f65f67330c28f-8383268-1327104-16782d85fb1b35%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216782d85fb025a-0f65f67330c28f-8383268-1327104-16782d85fb1b35%22%7D'}
testurl = 'http://insighttest05.jingdata.com'

alphaheaders = { 'Cookie': 'insight_uid=566; laravel_session=ZUo7Pm7uU7LIHUL0b7wDVrnPpfZPbqCLoA55WUF0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22566%22%2C%22%24device_id%22%3A%2216782d85fb025a-0f65f67330c28f-8383268-1327104-16782d85fb1b35%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216782d85fb025a-0f65f67330c28f-8383268-1327104-16782d85fb1b35%22%7D'}#alph,
#alpha

#headers = {'Cookie':'acw_tc=3ccdc15215435988465487129e53b8fc7adc273e227d84dfc69f330ce72595; dfp=CirvoHIC3wUNPhzjneMzi5pyHo36SWhGeXc7sJq6KOKmxCT1MM4x+QzSsy+9a3KQ2iYTvVzb3b7214yqhqf4T0n/uXvGDOAi0f+eHNtvAAsSEDOGmQPC5v83Op8zanH2BvwqTCYuzPf156ZzdaRwbPevmdN4z8Q8oUhxHPlGE5w%3D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22357%22%2C%22%24device_id%22%3A%2216782d85fb025a-0f65f67330c28f-8383268-1327104-16782d85fb1b35%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216782d85fb025a-0f65f67330c28f-8383268-1327104-16782d85fb1b35%22%7D; insight_uid=794; laravel_session=z8yhkJiyvNRhGJgOgDEPoWanXIAn5xTkaqgV4nSm'}
#生产环境Cookie

alphaurl = "http://insight-alpha.jingdata.com"
url = "https://insight.jingdata.com"

loginurl = url + '/api/user/login'
data = {"mobile":"15200000001","password":"jingdata123456","is_remember":"1"}
r =requests.post(loginurl,data)
d = r.json()
x0 = r.cookie
x1 = r.cookies['acw_tc']
#x2 = r.cookies['insight_uid']
x3 = r.cookies['laravel_session']
#headers = {"Cookie": x0}
print(x0)
headers = {"Cookie":'laravel_session=' + x3 + ';insight_uid=15621' + ';acw_tc=' + x1}
print(headers)

#print(headers)
