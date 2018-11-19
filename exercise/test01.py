import unittest
import HTMLTestRunner
import requests
import json
import pymysql
from config.url import url,headers
from config import gl
from unittest import TestLoader,TestSuite,TestCase

class HeaderselectTest(unittest.TestCase):

    def test_name_select(self): #高级检索-表头字段筛选-公司简称
        global cid
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"name.or\":[\"阿里巴巴\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('公司简称输入阿里巴巴关键词筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)
        print(d['data']['data'][0]['id'])
        cid = d['data']['data'][0]['id']
        return cid

        #gl.companyid = d['data']['data'][0]['id']

    def test_companyindex(self): #项目详情页


        print(cid)

if '__name__' == '__main__':
    unittest.main