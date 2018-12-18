import unittest
import requests
import json
from config.url import url,headers
from config.gl import *
import pymysql

class LibraryTest(unittest.TestCase):

    # 指标库首页
    def test_library_index(self):
        library_url = url + '/api/macro/index'
        r = requests.get(library_url,headers = headers)
        d =r.json()
        hot = len(d['data']['hot'])
        print(r.status_code)
        self.assertEqual(hot,10)

    # 左侧Menu
    def test_library_path(self):
        library_path_url = url + '/api/macro/path'
        r = requests.get(library_path_url,headers = headers)
        d = r.json()
        menu = d['data'][0]['name']
        print('【指标库左侧第一个Menu是：',menu,'】')
        self.assertEqual(len(d['data']),4)

    # 指标库搜索关键词美拍
    def test_library_search(self):
        library_search_url = url + '/api/macro/list?source=indexlibrary&keyword=美拍&pageSize=20&curPage=1'
        r = requests.get(library_search_url,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('指标库搜索美拍匹配的结果有',x,'条】')
        self.assertGreaterEqual(x,10000)

    # 新经济行业—新科技子目录
    def test_library_pathdir001(self):
        library_dir_url = url + '/api/macro/path?id=' + str(id001)
        r = requests.get(library_dir_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【新经济行业—新科技下子级目录有：',x,'个】')
        self.assertEqual(r.status_code,200)

    # 新经济行业—新科技—大数据子级目录
    def test_library_pathdir002(self):
        library_dir_url = url + '/api/macro/path?id=' + str(id002)
        r = requests.get(library_dir_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【新经济行业—新科技—大数据下子级目录有：',x,'个】')
        self.assertEqual(r.status_code,200)

    # 新经济行业—新科技—大数据—国内大数据市场规模指标列表
    def test_library_list(self):
        library_list_url = url + '/api/macro/list?id=' + str(id003) + '&pageSize=20&curPage=1'
        r = requests.get(library_list_url,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【新经济行业—新科技—大数据—国内大数据市场规模指标有：',x,'条】')
        self.assertEqual(r.status_code,200)

    # 新经济行业—新科技—大数据—国内大数据市场规模指标详情
    def test_library_detail(self):
        library_detail_url = url + '/api/macro/detail?id=' + str(id004)
        r = requests.get(library_detail_url, headers = headers)
        d = r.json()
        x = d['data']['name']
        print('【该指标数据标题为：',x,'】')
        self.assertEqual(r.status_code,200)

    # 新经济行业—新科技—大数据—国内大数据市场规模指标—市场规模：大数据：中国
    def test_library_download(self):
        library_download_url = url + '/api/macro/download?id=' + str(9607081) + '&timezone=-8'
        r = requests.get(library_download_url,headers = headers)
        if (r.status_code == 200):
            print('【新经济行业—新科技—大数据—国内大数据—市场规模：大数据：中国—导出成功')
        else:
            print('【新经济行业—新科技—大数据—国内大数据—市场规模：大数据：中国—导出失败】')
        self.assertEqual(r.status_code,200)




if __name__ == '__main__':
    unittest.main()