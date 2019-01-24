import unittest
import requests
import json
from config.url import url,headers
from config.gl import *
import pymysql
import urllib,urllib3

class LibraryTest(unittest.TestCase):
    '''指标库'''

    def test_library_index(self):
        '''指标库首页—热门指标'''
        library_url = url + '/api/macro/index'
        r = requests.get(library_url,headers = headers)
        d =r.json()
        hot = len(d['data']['hot'])
        print('【指标库首页—热门指标数量为：',hot,'】')
        self.assertEqual(hot,10)

    def test_library_index_recent(self):
        '''指标库首页—最近更新指标/api/macro/index'''
        library_url = url + '/api/macro/index'
        r = requests.get(library_url,headers = headers)
        d =r.json()
        x = len(d['data']['recent'])
        print('【指标库首页—最近更新指标数量为：',x,'】')
        #self.assertEqual(x,10)

    def test_library_path(self):
        '''左侧Menu'''
        library_path_url = url + '/api/macro/path'
        r = requests.get(library_path_url,headers = headers)
        d = r.json()
        menu = d['data'][0]['name']
        print('【指标库左侧第一个Menu是：',menu,'】')
        self.assertEqual(len(d['data']),4)

    def test_library_search(self):
        '''指标库搜索关键词美拍'''
        library_search_url = url + '/api/macro/list?source=indexlibrary&keyword=美拍&pageSize=20&curPage=1'
        r = requests.get(library_search_url,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【指标库搜索美拍匹配的结果有',x,'条】')
        self.assertGreaterEqual(x,10000)

    def test_library_pathdir001(self):
        '''新经济行业—新科技子目录'''
        library_dir_url = url + '/api/macro/path?id=' + str(id001)
        r = requests.get(library_dir_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【新经济行业—新科技下子级目录有：',x,'个】')
        self.assertEqual(r.status_code,200)

    def test_library_pathdir002(self):
        '''新经济行业—新科技—大数据子级目录'''
        library_dir_url = url + '/api/macro/path?id=' + str(id002)
        r = requests.get(library_dir_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【新经济行业—新科技—大数据下子级目录有：',x,'个】')
        self.assertEqual(r.status_code,200)

    def test_library_list(self):
        '''新经济行业—新科技—大数据—国内大数据市场规模指标列表'''
        library_list_url = url + '/api/macro/list?id=' + str(id003) + '&pageSize=20&curPage=1'
        r = requests.get(library_list_url,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【新经济行业—新科技—大数据—国内大数据市场规模指标有：',x,'条】')
        self.assertEqual(r.status_code,200)

    def test_library_detail(self):
        '''新经济行业—新科技—大数据—国内大数据市场规模指标详情'''
        library_detail_url = url + '/api/macro/detail?id=' + str(id004)
        r = requests.get(library_detail_url, headers = headers)
        d = r.json()
        x = d['data']['name']
        print('【该指标数据标题为：',x,'】')
        self.assertEqual(r.status_code,200)

    def test_library_download(self):
        '''新经济行业—新科技—大数据—国内大数据市场规模指标—市场规模：大数据：中国'''
        library_download_url = url + '/api/macro/download?id=' + str(9607081) + '&timezone=-8'
        r = requests.get(library_download_url,headers = headers)
        if (r.status_code == 200):
            print('【新经济行业—新科技—大数据—国内大数据—市场规模：大数据：中国—导出成功】')
        else:
            print('【新经济行业—新科技—大数据—国内大数据—市场规模：大数据：中国—导出失败】')
        self.assertEqual(r.status_code,200)

    def test_library_china_macro(self):
        '''指标库—中国宏观子目录'''
        library_macro_url = url + '/api/macro/path?id=' + str(id005)
        r = requests.get(library_macro_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【指标库—中国宏观—子目录有:',x,'个】')
        self.assertGreaterEqual(x,17)

    def test_library_macro(self):
        '''指标库—中国宏观—人民生活—子目录'''
        library_macro_url = url + '/api/macro/path?id=' + str(id006)
        r = requests.get(library_macro_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【指标库—中国宏观—人民生活—子目录有:', x, '个】')
        self.assertGreaterEqual(x, 5)

    def test_library_macro001(self):
        '''指标库—宏观经济—中国宏观—人民生活—人民生活质量'''
        library_macro001_url = url + '/api/macro/path?id=' + str(id007)
        r = requests.get(library_macro001_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【指标库—宏观经济—中国宏观—人民生活—人民生活质量:', x, '个】')
        self.assertGreaterEqual(x, 2)

    def test_library_macro002(self):
        '''指标库—宏观经济—中国宏观—人民生活—人民生活质量—电话普及率（月）'''
        library_macro002_url = url + '/api/macro/list?id=' + str(id008) + '&pageSize=20&curPage=1'
        r = requests.get(library_macro002_url,headers = headers)
        d = r.json()
        x = len(d['data']['list'])
        print('【指标库—宏观经济—电话普及率（月）指标有:', x, '个】')
        self.assertGreaterEqual(x, 2)

    def test_library_macro002_download(self):
        '''指标库—宏观经济—中国宏观—人民生活—人民生活质量—电话普及率（月）—Excel下载'''
        library_macro002_download_url = url + '/api/macro/download?id=' + str(id009) + '&timezone=-8'
        r = requests.get(library_macro002_download_url,headers = headers)
        if r.status_code == 200:
            print('【指标库—宏观经济—电话普及率（月）指标下载成功】')
        else:
            print('【指标库—宏观经济—电话普及率（月）指标下载失败】')
        self.assertGreaterEqual(r.status_code,200)

    def test_library_detail(self):
        '''中国宏观—详情页'''
        library_detail_url = url + '/api/macro/detail?id=' + str(id009)
        r = requests.get(library_detail_url,headers = headers)
        d = r.json()
        x = len(d['data']['line_chart_value_datas'])
        print('【中国宏观—电话普及率（月）指标详情页打开成功】')
        self.assertEqual(x,173)

    def test_library_official_account(self):
        '''指标库—特色数据—公众号数据台账'''
        library_official_account_url = url + '/api/macro/path?id=' + str(id010)
        r = requests.get(library_official_account_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【指标库—特色数据—公众号数据有:', x, '条】')
        self.assertGreaterEqual(x, 24)

    def test_library_wealth(self):
        '''指标库—特色数据—公众号数据—财富台账'''
        library_wealth_url = url + '/api/macro/ledgerList?id=' +  str(id011) + '&ledger=official_account&sort={"field":"read_count","order":"desc"}&pageSize=20&curPage=1'
        r = requests.get(library_wealth_url,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【指标库—特色数据—公众号数据—财富台账有:', x, '个公众号】')
        self.assertGreaterEqual(x, 1200)

    def test_library_wealth_path(self):
        '''指标库—特色数据—公众号数据—财富台账—平安普惠指标'''
        library_wealth_path_url = url + '/api/macro/list?id=' + str(id012) + '&pageSize=20&curPage=1'
        r = requests.get(library_wealth_path_url,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【指标库—特色数据—公众号数据—财富-平安普惠有:', x, '指标】')
        self.assertGreaterEqual(x, 3)



if __name__ == '__main__':
    unittest.main()