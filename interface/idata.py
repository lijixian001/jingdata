import unittest
import requests
import json
from config.url import url,headers
import pymysql

config = {
    'host': "192.168.6.38",
    'user': "db-test",
    'password': "123456",
    'db': "jingdata_saas"
}
# 参数有个默认名字（请根据自己实际修改）
def loadDataBaseFromMyServer(database='jingdata_saas'):
    # 打开数据库连接
    db = pymysql.connect(**config)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    try:
        cursor.execute("select id from banner order by updated_at desc limit 0,1 " )
        # 使用 fetchall() 方法获取所有数据，获取结果是一个二维tuple
        data = cursor.fetchone()
    except BaseException as e:
        print(e)
        db.rollback()
    db.close()
    return data

class InsightDataTest(unittest.TestCase):

    def test_menu(self): #洞见数据menu
        menu_url = url + '/api/insight/menu'
        r = requests.get(menu_url,headers = headers)
        d = r.json()
        x = len(d['data'][0]['children'])
        print('【洞见数据左侧菜单栏第一个Menu有',x,'不同类型的公司列表】')
        self.assertEqual(x,6)

    def test_allcompany(self):#全部公司列表
        allcompany_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
                "object": "company",
                "curPage": 1,
                "pageSize": 20,
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
                }
        r = requests.post(allcompany_url,data,headers = headers)
        d = r.json()
        print("全部公司数量 ： %s"%(d['data']['total']))
        self.assertEqual(len(d['data']['data']),20)

    def test_showFieldsCompany(self):#默认展示表头字段
        allcompany_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
                "object": "company",
                "curPage": 1,
                "pageSize": 20,
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
                }
        r = requests.post(allcompany_url,data,headers = headers)
        d = r.json()
        print('默认展示表头字段为 ： %s'%(len(d['data']['showFieldsCompany'])))
        self.assertEqual(len(d['data']['showFieldsCompany']),12)

    def test_selectFieldsCompany(self):#可筛选表头字段
        allcompany_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
                "object": "company",
                "curPage": 1,
                "pageSize": 20,
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
                }
        r = requests.post(allcompany_url,data,headers = headers)
        d = r.json()
        print('可筛选表头字段数量为： %s'%len(d['data']['selectFieldsCompany']))
        self.assertEqual(len(d['data']['selectFieldsCompany']),18)

    def test_allFieldsCompany(self):#全部表头字段
        allcompany_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
                "object": "company",
                "curPage": 1,
                "pageSize": 20,
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
                }
        r = requests.post(allcompany_url,data,headers = headers)
        d = r.json()
        print('全部表头字段数量为： %s'%len(d['data']['allFieldsCompany']))
        self.assertEqual(len(d['data']['allFieldsCompany']),30)

    def test_selectFieldsdict(self):#可筛选字段字典
        allcompany_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
                "object": "company",
                "curPage": 1,
                "pageSize": 20,
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
                }
        r = requests.post(allcompany_url,data,headers = headers)
        d = r.json()
        print('可筛选字段字典【行业】数量为： %s' % len(d['data']['charts']['finance_phase']['buckets']))
        print('可筛选字段字典【所在地】数量为： %s'%len(d['data']['charts']['address1']['buckets']))
        print('可筛选字段字典【最近融资轮次】数量为： %s' % len(d['data']['charts']['address1']['buckets']))
        self.assertEqual(len(d['data']['charts']['industry']['buckets']),28)
        self.assertEqual(len(d['data']['charts']['address1']['buckets']),60)
        self.assertEqual(len(d['data']['charts']['finance_phase']['buckets']),20)

    def test_search_example(self): #检索示例
        search_example_url = url + "/api/upgradefilter/getprefabricatedcondition?type=100"
        r = requests.get(search_example_url,headers = headers)
        d = r.json()
        print('检索示例名称 ： %s'%(d['data'][0]['name']),(d['data'][1]['name']))
        self.assertEqual(d['data'][0]['name'],'腾讯投资的全部项目')
        self.assertEqual(d['data'][1]['name'],'阿里巴巴并购的项目')

    def test_phase_dict(self): #高级检索-最近融资轮次字典
        phase_dict_url = url + "/api/redis/dictcache?type=2&key=crm-dict_phase"
        r = requests.get(phase_dict_url,headers = headers)
        d = r.json()
        print('高级检索-最近融资轮次字典数量 : %s'%len(d['data']))
        self.assertEqual(len(d['data']),22)

    def test_industry_dict(self): #高级检索-行业字典数量
        industry_idct_url = url + "/api/redis/dictcache?type=2&key=crm-dict_industry"
        r = requests.get(industry_idct_url,headers = headers)
        d = r.json()
        print('高级检索-行业字典数量 ： %s'%len(d['data']))
        self.assertEqual(len(d['data']),28)

    def test_address_dict(self): #高级检索-所在地
        address_dict_url = url + '/api/search/tagaddress?type=2&name=0'
        r = requests.get(address_dict_url,headers = headers)
        d = r.json()
        print('高级检索-所在地一级行政区数量为： %s'%len(d['data']),'个')
        self.assertEqual(len(d['data']),35)

    def test_tagstree(self): #高级检索-标签
        tagstree_url = url + '/api/search/gettagstree'
        r = requests.get(tagstree_url,headers = headers)
        d = r.json()
        print('高级检索-标签树数量为： %s'%len(d['data']))
        self.assertEqual(len(d['data']),28)

    def test_getdefaulttagwebsite(self): #高级检索-报道媒体
        getdefaulttagwebsite_url = url + '/api/search/getdefaulttagwebsite?type=0'
        r = requests.get(getdefaulttagwebsite_url,headers =headers)
        d = r.json()
        print('高级检索-报道媒体数量为： %s'%len(d['data']),'个')
        print('第一序列报道媒体为： %s'%d['data'][0])
        self.assertEqual(len(d['data']),6)
        self.assertEqual(d['data'][0],'36氪')

    def test_dictbyobject(self): #高级检索-第一个下拉框选项
        dictbyobject_url = url + '/api/upgradefilter/dictbyobject?object=company&parent_id=458'
        r = requests.get(dictbyobject_url,headers = headers)
        d = r.json()
        print('高级检索-第一个下拉框内选项有 ： %s'%len(d['data']),'个')
        self.assertEqual(len(d['data']),3)

class HeaderselectTest(unittest.TestCase):

    def test_name_select(self): #高级检索-表头字段筛选-公司简称
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"name.or\":[\"阿里巴巴\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('公司简称输入阿里巴巴关键词筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)

    def test_name_select_pull(self): #高级检索-表头字段筛选-公司简称-下拉选项
        name_select_url = url + '/api/upgradefilter/getreleatenamebykey?object=company&name=阿里巴巴'
        r = requests.get(name_select_url,headers = headers)
        d = r.json()
        print('公司简称字段筛选下拉选项数量： %s'%len(d['data']))
        self.assertEqual(len(d['data']),10)

    def test_phase_select(self): #高级检索-表头字段筛选-最近融资轮次
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.latest_phase.or\":[30,40]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('最近融资轮次输入A轮、B轮筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)

    def test_time_select(self): #高级检索-表头字段筛选-最近融资时间
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.latest_finance_date\":[\"2018-10-01\",\"2018-10-31\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('最近融资时间为10月份的筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)

    def test_industry_select(self): #高级检索-表头字段筛选-行业
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"industry.or\":[1]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('行业是电商的筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)

    def test_industry_select(self): #高级检索-表头字段筛选-所在地
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"address.or\":[101]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('所在地是北京的筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)

    def test_address_dict(self): #高级检索-所在地-字典
        address_dict_url = url + '/api/search/tagaddress?type=2&name=0'
        r = requests.get(address_dict_url,headers = headers)
        d = r.json()
        print('高级检索-所在地一级行政区数量为： %s'%len(d['data']),'个')
        self.assertEqual(len(d['data']),35)

    def test_brief_select(self): #高级检索-表头字段筛选-一句话简介
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"address.or\":[],\"brief.or\":[\"电商\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('一句话简介包含电商的筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)

    def test_finance_select(self): #高级检索-表头字段筛选-最近一轮融资额
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.latest_finance_amount\":[\"1000\",\"1000\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('最近一轮融资额等于1000W人民币的筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)

    def test_historyfinance_select(self): #高级检索-表头字段筛选-历史总融资额
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.total_finance_amount\":[3300,3300]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('历史总融资额等于500W美元的筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)

    def test_valuation_select(self): #高级检索-表头字段筛选-估值
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.latest_valuation\":[\"1000\",\"\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('估值大于1000W人民币的筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)

    def test_starttime_select(self):
        #高级检索-表头字段筛选-创办时间
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{},{\"stat_investment.latest_valuation\":[null,\"\"],\"start_date\":[\"2017-01-01\",\"2017-12-31\"]}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url,data,headers = headers)
        d = r.json()
        print('创办时间是去年的筛选结果为： %s'%(d['data']['total']),'条')
        self.assertEqual(len(d['data']['data']),20)

class HeadersortTest(unittest.TestCase): #全部公司列表表头字段排序

    def test_hot_score_desc(self): #表头字段排序-热度-降序Desc
        headersort_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_score\",\"param\":[\"desc\"]}]}"}
        r = requests.post(headersort_url,data,headers = headers)
        d = r.json()
        print('全部公司列表热度最高公司名称、及热度值为： %s'%(d['data']['data'][0]['name']),'、%s'%(d['data']['data'][0]['stat_rank.hot_score']))
        self.assertGreaterEqual(d['data']['data'][0]['stat_rank.hot_score'],d['data']['data'][1]['stat_rank.hot_score'])

    def test_hot_score_asc(self): #表头字段排序-热度-升序Asc
        headersort_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_score\",\"param\":[\"asc\"]}]}"}
        r = requests.post(headersort_url,data,headers = headers)
        d = r.json()
        print('全部公司列表热度最低公司名称、及热度值为： %s'%(d['data']['data'][0]['name']),'、%s'%(d['data']['data'][0]['stat_rank.hot_score']))
        self.assertGreaterEqual(d['data']['data'][2]['stat_rank.hot_score'],d['data']['data'][1]['stat_rank.hot_score'])

    def test_hot_trend_desc(self): #表头字段排序-热度趋势-降序Desc
        headerhot_trend_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(headerhot_trend_url,data,headers = headers)
        d = r.json()
        print('全部公司列表热度趋势最高公司名称、及热度趋势值为： %s'%(d['data']['data'][0]['name']),'、%s'%(d['data']['data'][0]['stat_rank.hot_trend']))
        self.assertGreaterEqual(d['data']['data'][0]['stat_rank.hot_trend'],d['data']['data'][1]['stat_rank.hot_trend'])

    def test_hot_trend_asc(self): #表头字段排序-热度趋势-升序Asc
        headerhot_trend_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"company","curPage":1,"pageSize":20,"search":"{\"company.and\":[{}]}","data":"{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"asc\"]}]}"}
        r = requests.post(headerhot_trend_url,data,headers = headers)
        d = r.json()
        print('全部公司列表热度趋势最低公司名称、及热度趋势值为： %s'%(d['data']['data'][0]['name']),'、%s'%(d['data']['data'][0]['stat_rank.hot_trend']))
        self.assertGreaterEqual(d['data']['data'][2]['stat_rank.hot_trend'],d['data']['data'][1]['stat_rank.hot_trend'])

    def test_new_economy(self): #新经济公司列表
        new_economy_url = url + '/api/company/search'
        data = {"curPage":1,"pageSize":20,"type":"new_economy","sort":"[{\"field\":\"market_value\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(new_economy_url,data,headers = headers)
        d = r.json()
        print('新经济公司数量为： %s'%(d['data']['total']))
        self.assertGreaterEqual(d['data']['total'],148)

    def test_c_industry(self): #新经济公司所属领域字典
        c_industry_url = url + '/api/insight/dict_data?type=c_industry'
        r = requests.get(c_industry_url,headers = headers)
        d = r.json()
        print('新经济公司所属领域字典有： %s'%len(d['data']),'个不同领域')
        self.assertEqual(len(d['data']),28)

    def test_c_area(self): #新经济公司所在地字典
        c_area_url = url + '/api/insight/dict_data?type=c_area'
        r = requests.get(c_area_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【新经济公司所在地字典有:',x ,'个一级地区】')
        self.assertEqual(x,35)




if __name__ == '__main__':
    unittest.main()