import unittest
import requests
import json
from config.url import url,headers
from config.gl import *
import pymysql

class ProjectDetailsTest(unittest.TestCase):

    # 阿里巴巴项目详情页
    def test_company_tab(self):
        company_url = url + '/api/company/tab?cid=' + str(albb_id)
        r = requests.get(company_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【阿里巴巴详情页Tab数量为：',x,'】')
        self.assertEqual(x,10)

    def test_company_index(self):
        company_url = url + '/api/company/index?cid=' + str(albb_id)
        r = requests.get(company_url,headers = headers)
        d = r.json()
        x = d['data']['list']['info']['cid']
        #x = d['data']['menu'][0]['title']
        print(x)
        self.assertEqual(x,str(albb_id))



if __name__ == '__main__':
    unittest.main()