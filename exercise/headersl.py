import requests
import json

#url = 'http://insight-alpha.jingdata.com/api/indexinfo/indexdata'
url = 'http://insight-alpha.jingdata.com/api/promotion/list?curPage=1&pageSize=10'
headers = {
    'Cookie':'Hm_lvt_066da718ccf0d5656b81620a125fd3d6=1535732957,1535964059,1536030135,1536232198; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22794%22%2C%22%24device_id%22%3A%2216440457a745cd-0f552fc053144e-47e1e39-1327104-16440457a75176%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216440457a745cd-0f552fc053144e-47e1e39-1327104-16440457a75176%22%7D; insight_token=dWlkPTc5NCZzaWQ9anc4UTBxbzdmekhIVDdkTldtbEIxd3REemZzR3FGdndlWDFsRTY5MA%3D%3D.2553fec3d4ebd4884705af081fa6560c.1542255703; insight_uid=794; laravel_session=jw8Q0qo7fzHHT7dNWmlB1wtDzfsGqFvweX1lE690'
}
r = requests.get(url,headers=headers)
dicts = json.loads(r.text)
print(dicts)
print(headers)
code = r.status_code
print(r.headers)