import unittest
import requests
import json
#from config.url import url,headers
from config.url import *
from config.gl import *
import pymysql
import sys

class WorkbenchTest(unittest.TestCase):
    '''工作台'''
    def test_folderlist(self):
        '''工作台收藏夹列表
        /api/userscollection/folderlist'''
        folderlist_url = url + '/api/userscollection/folderlist?type=1'
        r = requests.get(folderlist_url,headers = headers)
        d = r.json()
        x = len(d['data']['list'])
        print('【工作台—顶部Tab有：',x,'个】')
        self.assertEqual(d['data']['list'][0]['name'],'推荐公司')
        x1 = d['data']['list'][0]['id']

    def test_work_datalist(self):
        '''工作台—推荐公司列表'''
        datalist_url = url + '/api/userscollection/datalist'
        payload = {"pageSize":30,"curPage":1,"floder_id":"46088","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(datalist_url,data=payload,headers = headers)
        d = r.json()
        self.assertGreaterEqual(r.status_code,200)
        x1 = len(d['data']['list'])
        print('【推荐公司公司有：',x1,'家】')
        self.assertGreaterEqual(x1,15)

    def test_work_datalist001(self):
        '''工作台—推荐公司列表—收藏夹id为空'''
        datalist_url = url + '/api/userscollection/datalist'
        payload = {"pageSize":30,"curPage":1,"floder_id":"","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(datalist_url,data=payload,headers = headers)
        d = r.json()
        self.assertGreaterEqual(d['code'],'1001')
        print('【收藏夹id为空时 code = ',d['code'],'】')

    def test_work_c_indusry(self):
        '''推荐公司所属行业字典'''
        work_c_industry_url = url + '/api/insight/dict_data?type=c_industry'
        r = requests.get(work_c_industry_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【推荐公司所属行业有：',x,'个】')
        self.assertEqual(x,28)

    def test_work_c_area(self):
        '''推荐公司所在地字典'''
        work_c_area_url = url + '/api/insight/dict_data?type=c_area'
        r = requests.get(work_c_area_url, headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【推荐公司所在地一级行政地区有：', x, '个】')
        self.assertEqual(x, 35)

    def test_work_insightdatafolder(self):
        '''阿里健康收藏信息'''
        insightdatafolder_url = url + '/api/userscollection/insightdatafolder?type=1&insight_id=' + str(aljk_id)
        r = requests.get(insightdatafolder_url,headers = headers)
        d = r.json()
        x = d['data']['list'][0]['name']
        self.assertEqual(x,'我的收藏')

    def test_work_operationdata_add(self):
        '''推荐公司添加至我的收藏'''
        operationdata_url = url + '/api/userscollection/operationdata'
        data = {"type":1,"add":"[{\"floder_id\":46088,\"values\":[8465]}]","delete":"[]"}
        r = requests.post(operationdata_url,data,headers = headers)
        if r.status_code == 200:
            print('【公司添加至我的收藏成功】')
        else:
            print('【公司添加至我的收藏失败】')
        self.assertEqual(r.status_code,200)

    def test_work_operationdata_delete(self):
        '''推荐公司移出我的收藏'''
        operationdata_url = url + '/api/userscollection/operationdata'
        data = {"type":1,"add":"[]","delete":"[{\"floder_id\":2382,\"values\":[8465]}]"}
        r = requests.post(operationdata_url,data,headers = headers)
        if r.status_code == 200:
            print('【公司移出我的收藏成功】')
        else:
            print('【公司移出我的收藏失败】')
        self.assertEqual(r.status_code,200)

    def test_work_folder_add(self):
        '''新建自定义收藏夹'''
        global fid
        add_folder_url = url + '/api/userscollection/addcollectionfolder'
        data = {"type":1,"name":"新建收藏夹"}
        r = requests.post(add_folder_url,data,headers = headers)
        d = r.json()
        x = d['data']['name']
        print('【添加的自定义收藏夹名称为：',x,'】')
        self.assertEqual(x,'新建收藏夹')
        fid = d['data']['id']

    def test_work_folder_del(self):
        '''删除自定义收藏夹'''
        del_folder_url = url + '/api/userscollection/deletecollectionfolder?id=' + str(fid)
        r = requests.get(del_folder_url,headers = headers)
        if r.status_code == 200:
            print('【自定义收藏夹删除成功】')
        else:
            print('【自定义收藏夹删除失败】')
        self.assertEqual(r.status_code,200)

    def test_work_note_a_select(self):
        '''阿里健康的笔记列表'''
        global noteid001
        notelist_url  =  url + '/api/userscollection/notelist?type=1&insight_id=' + str(aljk_id) + '&folder_id=0'
        r = requests.get(notelist_url,headers = headers)
        d = r.json()
        noteid001 = d['data'][0]['id']
        self.assertEqual(r.status_code,200)

    def test_work_note_b_del(self):
        '''阿里健康删除笔记'''
        add_note_url  =  url + '/api/userscollection/deletecollectionnote'
        data = {"id":noteid001,"insight_id":"8465"}
        r = requests.post(add_note_url,data,headers = headers)
        d = r.json()
        self.assertEqual(r.status_code,200)

    def test_work_note_c_add(self):
        '''阿里健康添加笔记'''
        add_note_url  =  url + '/api/userscollection/addcollectionnote'
        data = {"type":1,"insight_id":aljk_id,"folder_id":0,"content":"\"addnote\""}
        r = requests.post(add_note_url,data,headers = headers)
        d = r.json()
        noteid = d['data']['id']
        print('【阿里健康添加的笔记 id =',noteid,'】')
        self.assertEqual(r.status_code,200)

    def test_work_exportnum(self):
        '''推荐公司列表导出统计'''
        work_exportnum_url = url + '/api/userscollection/searchexportnum'
        data = {"type":1,"sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]","search":"[]","floder_id":"46088"}
        r = requests.post(work_exportnum_url,json = data,headers = headers)
        d = r.json()
        x = d['data']['max_limit_num']
        print('【剩余可导出条数为：',d['data']['export_num'],'】')
        self.assertGreaterEqual(x,5000)

    def test_work_down(self):
        '''推荐公司导出'''
        work_down_url = url + '/api/userscollection/searchexport'
        data = {"curPage":1,"pageSize":30,"timezone":-8,"efields":"[{\"name\":\"公司简称\",\"field\":\"name\"},{\"name\":\"最新市值/估值\",\"field\":\"market_value\"},{\"name\":\"所属领域\",\"field\":\"industry\"},{\"name\":\"一句话简介\",\"field\":\"short_description\"},{\"name\":\"成立时间\",\"field\":\"establish_date\"},{\"name\":\"所在地\",\"field\":\"address\"},{\"name\":\"私募股权融资总额\",\"field\":\"pe_financing_amount\"},{\"name\":\"资本市场\",\"field\":\"stock_market_short_name\"},{\"name\":\"IPO募集金额\",\"field\":\"ipo_financing_amount\"},{\"name\":\"上市时间\",\"field\":\"listed_date\"},{\"name\":\"配股与定增总额\",\"field\":\"share_placement_amount\"},{\"name\":\"年营业额\",\"field\":\"annual_turnover\"},{\"name\":\"年利润额\",\"field\":\"annual_profit\"},{\"name\":\"最新股价\",\"field\":\"close_price\"},{\"name\":\"最新涨跌幅\",\"field\":\"change_price_pct\"},{\"name\":\"P/E(TTM)\",\"field\":\"pe_ttm\"},{\"name\":\"P/B(LF)\",\"field\":\"pb\"},{\"name\":\"P/S(TTM)\",\"field\":\"ps\"}]","export_num":15,"type":1,"sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]","search":"[]","floder_id":"46088"}
        r = requests.post(work_down_url,data,headers = headers)
        if r.status_code == 200:
            print('【推荐公司导出成功】')
        else:
            print('【推荐公司导出成功】')
        self.assertEqual(r.status_code,200)

if __name__ ==  '__main__':
    unittest.main()






