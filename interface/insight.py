import unittest
import requests
import json
from config.url import url,headers
import pymysql
from config.sql import *

class InsightTest(unittest.TestCase):
    '''公司交易（原）'''
    # 洞见数据menu
    def test_idata_menu(self):
        menu_url = url + '/api/insight/menu'
        r = requests.get(menu_url, headers=headers)
        d = r.json()
        x = len(d['data'][0]['children'])
        print('【洞见数据左侧菜单栏第一个Menu有', x, '不同类型的公司列表】')
        self.assertEqual(x, 6)

    # 全部公司列表
    def test_all_company(self):
        all_company_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
            "object": "company",
            "curPage": 1,
            "pageSize": 20,
            "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
        }
        r = requests.post(all_company_url, data, headers=headers)
        d = r.json()
        print("【全部公司数量为 ： %s" % (d['data']['total']), '家】')
        self.assertEqual(len(d['data']['data']), 20)

    # 全部公司列表表头字段
    def test_all_company_allFieldsCompany(self):
        all_company_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
            "object": "company",
            "curPage": 1,
            "pageSize": 20,
            "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
        }
        r = requests.post(all_company_url, data, headers=headers)
        d = r.json()
        print('【全部公司列表全部表头字段为： %s' % len(d['data']['allFieldsCompany']), '】')
        self.assertEqual(len(d['data']['allFieldsCompany']), 30)

    # 全部公司可筛选表头字段
    def test_all_company_selectFieldsCompany(self):
        all_company_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
            "object": "company",
            "curPage": 1,
            "pageSize": 20,
            "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
        }
        r = requests.post(all_company_url, data, headers=headers)
        d = r.json()
        print('【全部公司可筛选表头字段为： %s' % len(d['data']['selectFieldsCompany']), '】')
        self.assertEqual(len(d['data']['selectFieldsCompany']), 18)

    # 全部公司默认展示表头字段
    def test_all_company_showFieldsCompany(self):
        all_company_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
            "object": "company",
            "curPage": 1,
            "pageSize": 20,
            "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
        }
        r = requests.post(all_company_url, data, headers=headers)
        d = r.json()
        print('【全部公司列表默认展示表头字段为 ： %s' % (len(d['data']['showFieldsCompany'])), '】')
        self.assertEqual(len(d['data']['showFieldsCompany']), 12)

    # 全部公司列表可筛选字段字典
    def test_all_company_selectFieldsdict(self):
        all_company_url = url + "/api/upgradefilter/getsearchdatabyobject"
        data = {
            "object": "company",
            "curPage": 1,
            "pageSize": 20,
            "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"
        }
        r = requests.post(all_company_url, data, headers=headers)
        d = r.json()
        print('【全部公司可筛选字段字典【行业】数量为： %s' % len(d['data']['charts']['finance_phase']['buckets']), '】')
        print('【全部公司可筛选字段字典【所在地】数量为： %s' % len(d['data']['charts']['address1']['buckets']), '】')
        print('【全部公司可筛选字段字典【最近融资轮次】数量为： %s' % len(d['data']['charts']['address1']['buckets']), '】')
        self.assertEqual(len(d['data']['charts']['industry']['buckets']), 28)
        self.assertEqual(len(d['data']['charts']['address1']['buckets']), 60)
        self.assertEqual(len(d['data']['charts']['finance_phase']['buckets']), 20)

    # 全部公司列表检索示例
    def test_search_example(self):
        search_example_url = url + "/api/upgradefilter/getprefabricatedcondition?type=100"
        r = requests.get(search_example_url, headers=headers)
        d = r.json()
        print('【检索示例名称 ： %s' % (d['data'][0]['name']), (d['data'][1]['name']), '】')
        self.assertEqual(d['data'][0]['name'], '腾讯投资的全部项目')
        self.assertEqual(d['data'][1]['name'], '阿里巴巴并购的项目')

    # 高级检索-所在地-字典
    def test_all_company_address_dict(self):
        address_dict_url = url + '/api/search/tagaddress?type=2&name=0'
        r = requests.get(address_dict_url, headers=headers)
        d = r.json()
        print('【高级检索-所在地一级行政区数量为： %s' % len(d['data']), '个】')
        self.assertEqual(len(d['data']), 35)

    # 高级检索-最近融资轮次字典
    def test_all_company_phase_dict(self):
        phase_dict_url = url + "/api/redis/dictcache?type=2&key=crm-dict_phase"
        r = requests.get(phase_dict_url, headers=headers)
        d = r.json()
        print('【高级检索-最近融资轮次字典数量 : %s' % len(d['data']), '】')
        self.assertEqual(len(d['data']), 22)

    # 高级检索-行业字典数量
    def test_all_company_industry_dict(self):
        industry_idct_url = url + "/api/redis/dictcache?type=2&key=crm-dict_industry"
        r = requests.get(industry_idct_url, headers=headers)
        d = r.json()
        print('【高级检索-行业字典数量 ： %s' % len(d['data']), '】')
        self.assertEqual(len(d['data']), 28)

    # 高级检索-标签
    def test_all_company_tagstree(self):
        tagstree_url = url + '/api/search/gettagstree'
        r = requests.get(tagstree_url, headers=headers)
        d = r.json()
        print('【高级检索-标签树数量为： %s' % len(d['data']), '】')
        self.assertEqual(len(d['data']), 28)

    # 高级检索-报道媒体
    def test_all_company_getdefaulttagwebsite(self):
        '''高级检索—报道媒体'''
        getdefaulttagwebsite_url = url + '/api/search/getdefaulttagwebsite?type=0'
        r = requests.get(getdefaulttagwebsite_url, headers=headers)
        d = r.json()
        print('【高级检索-报道媒体数量为： %s' % len(d['data']), '家】')
        # print('第一序列报道媒体为： %s'%d['data'][0])
        # self.assertEqual(len(d['data']),6)
        self.assertEqual(d['data'][0], '36氪')

    # 高级检索-第一个下拉框选项
    def test_all_company_dictbyobject(self):
        dictbyobject_url = url + '/api/upgradefilter/dictbyobject?object=company&parent_id=458'
        r = requests.get(dictbyobject_url, headers=headers)
        d = r.json()
        print('【高级检索-第一个下拉框内选项有 ： %s' % len(d['data']), '个】')
        self.assertEqual(len(d['data']), 3)

    # 全部公司表头字段筛选
    def test_all_company_select_name(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20,
                "search": "{\"company.and\":[{},{\"name.or\":[\"阿里巴巴\"]}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url, data, headers=headers)
        d = r.json()
        print('【公司简称输入阿里巴巴关键词筛选结果为： %s' % (d['data']['total']), '家】')
        self.assertEqual(len(d['data']['data']), 20)

    # 高级检索-表头字段筛选-公司简称-下拉选项
    def test_name_select_pull(self):
        name_select_url = url + '/api/upgradefilter/getreleatenamebykey?object=company&name=阿里巴巴'
        r = requests.get(name_select_url, headers=headers)
        d = r.json()
        print('【公司简称字段筛选下拉选项数量： %s' % len(d['data']), '】')
        self.assertEqual(len(d['data']), 10)

    # 高级检索-表头字段筛选-最近融资轮次
    def test_phase_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20,
                "search": "{\"company.and\":[{},{\"stat_investment.latest_phase.or\":[30,40]}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url, data, headers=headers)
        d = r.json()
        print('【最近融资轮次输入A轮、B轮筛选结果为： %s' % (d['data']['total']), '条】')
        self.assertEqual(len(d['data']['data']), 20)

    # 高级检索-表头字段筛选-最近融资时间
    def test_time_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20,
                "search": "{\"company.and\":[{},{\"stat_investment.latest_finance_date\":[\"2018-10-01\",\"2018-10-31\"]}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url, data, headers=headers)
        d = r.json()
        print('【最近融资时间为10月份的筛选结果为： %s' % (d['data']['total']), '条】')
        self.assertEqual(len(d['data']['data']), 20)

    # 高级检索-表头字段筛选-行业
    def test_industry_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20,
                "search": "{\"company.and\":[{},{\"industry.or\":[1]}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url, data, headers=headers)
        d = r.json()
        print('【行业是电商的筛选结果为： %s' % (d['data']['total']), '条】')
        self.assertEqual(len(d['data']['data']), 20)

    # 高级检索-表头字段筛选-所在地
    def test_industry_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20,
                "search": "{\"company.and\":[{},{\"address.or\":[101]}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url, data, headers=headers)
        d = r.json()
        print('【所在地是北京的筛选结果为： %s' % (d['data']['total']), '条】')
        self.assertEqual(len(d['data']['data']), 20)

    # 高级检索-表头字段筛选-一句话简介
    def test_description_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20,
                "search": "{\"company.and\":[{},{\"address.or\":[],\"brief.or\":[\"电商\"]}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url, data, headers=headers)
        d = r.json()
        print('【一句话简介包含电商的筛选结果为： %s' % (d['data']['total']), '条】')
        self.assertEqual(len(d['data']['data']), 20)

    # 高级检索-表头字段筛选-最近一轮融资额
    def test_finance_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20,
                "search": "{\"company.and\":[{},{\"brief.or\":[\"电商\"]}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url, data, headers=headers)
        d = r.json()
        print('【最近一轮融资额等于1000W人民币的筛选结果为： %s' % (d['data']['total']), '条】')
        self.assertEqual(len(d['data']['data']), 20)

    # 高级检索-表头字段筛选-历史总融资额
    def test_historyfinance_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20,
                "search": "{\"company.and\":[{},{\"stat_investment.total_finance_amount\":[3300,3300]}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url, data, headers=headers)
        d = r.json()
        print('【历史总融资额等于500W美元的筛选结果为： %s' % (d['data']['total']), '条】')
        self.assertEqual(len(d['data']['data']), 20)

    # 高级检索-表头字段筛选-估值
    def test_valuation_select(self):
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20,
                "search": "{\"company.and\":[{},{\"stat_investment.latest_valuation\":[\"1000\",\"\"]}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url, data, headers=headers)
        d = r.json()
        print('【估值大于1000W人民币的筛选结果为： %s' % (d['data']['total']), '条】')
        self.assertEqual(len(d['data']['data']), 20)

    def test_starttime_select(self):
        # 高级检索-表头字段筛选-创办时间
        name_select_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20,
                "search": "{\"company.and\":[{},{\"stat_investment.latest_valuation\":[null,\"\"],\"start_date\":[\"2017-01-01\",\"2017-12-31\"]}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(name_select_url, data, headers=headers)
        d = r.json()
        print('【创办时间是去年的筛选结果为： %s' % (d['data']['total']), '条】')
        self.assertEqual(len(d['data']['data']), 20)

    # 全部公司-表头字段-排序-热度-降序DESC
    def test_hot_score_desc(self):  # 表头字段排序-热度-降序Desc
        headersort_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20, "search": "{\"company.and\":[{}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_score\",\"param\":[\"desc\"]}]}"}
        r = requests.post(headersort_url, data, headers=headers)
        d = r.json()
        print('【全部公司列表热度最高公司名称、及热度值为： %s' % (d['data']['data'][0]['name']),
              '、%s' % (d['data']['data'][0]['stat_rank.hot_score']), '】')
        self.assertGreaterEqual(d['data']['data'][0]['stat_rank.hot_score'],
                                d['data']['data'][1]['stat_rank.hot_score'])

    # 全部公司-表头字段-排序-热度-升序ASC
    def test_hot_score_asc(self):
        headersort_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20, "search": "{\"company.and\":[{}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_score\",\"param\":[\"asc\"]}]}"}
        r = requests.post(headersort_url, data, headers=headers)
        d = r.json()
        print('【全部公司列表热度最低公司名称、及热度值为： %s' % (d['data']['data'][0]['name']),
              '、%s' % (d['data']['data'][0]['stat_rank.hot_score']), '】')
        self.assertGreaterEqual(d['data']['data'][2]['stat_rank.hot_score'],
                                d['data']['data'][1]['stat_rank.hot_score'])

    # 全部公司-表头字段-排序-热度趋势-降序DESC
    def test_hot_trend_desc(self):
        headerhot_trend_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20, "search": "{\"company.and\":[{}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"desc\"]}]}"}
        r = requests.post(headerhot_trend_url, data, headers=headers)
        d = r.json()
        print('【全部公司列表热度趋势最高公司名称、及热度趋势值为： %s' % (d['data']['data'][0]['name']),
              '、%s' % (d['data']['data'][0]['stat_rank.hot_trend']), '】')
        self.assertGreaterEqual(d['data']['data'][0]['stat_rank.hot_trend'],
                                d['data']['data'][1]['stat_rank.hot_trend'])

    # 全部公司-表头字段-排序-热度趋势-升序ASC
    def test_hot_trend_asc(self):
        headerhot_trend_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object": "company", "curPage": 1, "pageSize": 20, "search": "{\"company.and\":[{}]}",
                "data": "{\"sort\":[{\"field\":\"stat_rank.hot_trend\",\"param\":[\"asc\"]}]}"}
        r = requests.post(headerhot_trend_url, data, headers=headers)
        d = r.json()
        print('【全部公司列表热度趋势最低公司名称、及热度趋势值为： %s' % (d['data']['data'][0]['name']),
              '、%s' % (d['data']['data'][0]['stat_rank.hot_trend']), '】')
        self.assertGreaterEqual(d['data']['data'][2]['stat_rank.hot_trend'],d['data']['data'][1]['stat_rank.hot_trend'])

# 交易

    def test_investment(self):
        investment_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"investment","curPage":1,"pageSize":20,"data":"{\"sort\":[{\"field\":\"finance_date\",\"param\":[\"desc\"]}]}"}
        r = requests.post(investment_url,data,headers = headers)
        d = r.json()
        print('【全部交易数量为：',d['data']['total'],'条】')
        self.assertGreaterEqual(d['data']['total'],110000)

    # 全部交易—检索示例
    def test_investment_example(self):
        investemnt_url = url + '/api/upgradefilter/getprefabricatedcondition?type=101'
        r = requests.get(investemnt_url,headers = headers)
        d1 = r.json()['data'][0]['name']
        d2 = r.json()['data'][1]['name']
        print('【全部交易检索示例为:',d1,'、',d2,'】')
        self.assertEqual(r.status_code,200)

    # 全部交易—投资轮次字典
    def test_investment_dict_phase(self):
        investment_dict_url = url + '/api/redis/dictcache?type=2&key=crm-dict_phase'
        r = requests.get(investment_dict_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【全部交易投资轮次一共有：',x,'个】')
        self.assertEqual(x,22)

    # 全部交易—私募股权融资
    def test_investment002(self):
        investment_url = url + '/api/investment/search'
        data = {"curPage":1,"pageSize":20,"type":"pri_equity_fina","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(investment_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【私募股权融资事件数为:',x,'起】')
        self.assertGreaterEqual(x,80000)

    # 全部交易—私募股权融资投资轮次字典
    def test_investment_phase_dict(self):
        investment_phase_url = url + '/api/insight/dict_data?type=c_phase'
        r = requests.get(investment_phase_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【私募股权融资投资轮次一共有：',x,'个】')
        self.assertEqual(x,22)

    # 全部交易—私募股权融资导出统计
    def test_investment_exportnum(self):
        investment_exportnum_url = url + '/api/investment/searchExportNum'
        data = {"type":"pri_equity_fina","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[]","search":"[]"}
        r = requests.post(investment_exportnum_url,data,headers = headers)
        d = r.json()
        x = d['data']['export_num']
        print('【当前可导出条数为：',x,'条】')
        self.assertEqual(r.status_code,200)

    # 全部交易—私募股权融资—导出本页
    def test_investment_export(self):
        investment_export_url = url + '/api/investment/searchExport'
        data = {"curPage":1,"pageSize":20,"timezone":-8,"efields":"[{\"field\":\"company.name\",\"name\":\"公司简称\",\"data_type\":\"text\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"includes\",\"not_includes\",\"includes_all\"],\"sort_enabled\":true,\"search_enabled\":true},{\"field\":\"finance_phase\",\"name\":\"投资轮次\",\"data_type\":\"selection\",\"data_unit\":null,\"dict_type\":\"c_phase\",\"operation\":[\"includes\",\"not_includes\"],\"sort_enabled\":true,\"search_enabled\":true},{\"field\":\"finance_date\",\"name\":\"交易时间\",\"data_type\":\"date\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"gte\",\"lte\",\"between\",\"eq\",\"not_eq\"],\"sort_enabled\":true,\"search_enabled\":true},{\"field\":\"finance_amount\",\"name\":\"交易金额\",\"data_type\":\"amount\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"eq\",\"not_eq\",\"gte\",\"lte\",\"between\"],\"sort_enabled\":true,\"search_enabled\":true},{\"field\":\"total_investors\",\"name\":\"投资方\",\"data_type\":\"collection\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"includes\",\"not_includes\",\"includes_all\"],\"sort_enabled\":false,\"search_enabled\":true},{\"field\":\"valuation\",\"name\":\"投后估值\",\"data_type\":\"amount\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"gte\",\"lte\",\"eq\",\"not_eq\",\"between\"],\"sort_enabled\":true,\"search_enabled\":true},{\"field\":\"report_title\",\"name\":\"相关报道\",\"data_type\":\"text\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"includes\",\"not_includes\",\"includes_all\"],\"sort_enabled\":false,\"search_enabled\":true},{\"field\":\"expose_date\",\"name\":\"曝光时间\",\"data_type\":\"date\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"gte\",\"lte\",\"eq\",\"not_eq\",\"between\"],\"sort_enabled\":true,\"search_enabled\":true}]","export_num":20,"type":"pri_equity_fina","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"id\",\"operation\":\"includes\",\"values\":[\"208332\",\"208437\",\"208331\",\"208403\",\"208445\",\"208388\",\"208390\",\"208447\",\"208444\",\"208392\",\"208459\",\"208340\",\"208153\",\"208133\",\"208179\",\"208339\",\"208152\",\"208141\",\"208156\",\"208026\"],\"type\":\"predicate\"}]","search":"[]"}
        r = requests.post(investment_export_url,data,headers = headers)
        if (r.status_code == 200):
            print('【私募股权融资本页导出成功】')
        else:
            print('【私募股权融资本页导出失败】')
        self.assertEqual(r.status_code,200)

    # 全部交易—私募股权融资—投资轮次降序—Desc
    def test_incestment_sort(self):
        investment_sort_url = url + '/api/investment/search'
        data = {"curPage":1,"pageSize":20,"type":"pri_equity_fina","sort":"[{\"field\":\"finance_phase\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(investment_sort_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        if (r.status_code == 200):
            print('【全部交易—私募股权融资—投资轮次降序排列成功】')
        else:
            print('【全部交易—私募股权融资—投资轮次降序排列失败】')

        self.assertEqual(r.status_code,200)

    # 全部交易—并购
    def test_investment003(self):
        investment_url = url + '/api/investment/search'
        data = {"curPage":1,"pageSize":20,"type":"merger","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(investment_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        if (r.status_code == 200):
            print('【全部交易—并购事件有：',x,'条】')
        else:
            print('【全部交易—并购事件请求失败】')
        self.assertGreaterEqual(x,6000)

    # 全部交易—并购—导出统计
    def test_investment00_export_num(self):
        url003 = url + '/api/investment/searchExportNum'
        data = {"type":"merger","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[]","search":"[]"}
        r = requests.post(url003,data,headers = headers)
        d = r.json()
        x = d['data']['export_num']
        print('【当前可导出条数为：', x, '条】')
        self.assertEqual(r.status_code, 200)

    # 全部交易—并购—导出本页
    def test_investment003_export(self):
        ''' 全部交易—并购—导出本页 '''
        investment_export_url = url + '/api/investment/searchExport'
        data = {"curPage":1,"pageSize":20,"timezone":-8,"efields":"[{\"field\":\"company.name\",\"name\":\"公司简称\",\"data_type\":\"text\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"includes\",\"not_includes\",\"includes_all\"],\"sort_enabled\":true,\"search_enabled\":true},{\"field\":\"finance_date\",\"name\":\"交易时间\",\"data_type\":\"date\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"gte\",\"lte\",\"between\",\"eq\",\"not_eq\"],\"sort_enabled\":true,\"search_enabled\":true},{\"field\":\"finance_amount\",\"name\":\"交易金额\",\"data_type\":\"amount\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"eq\",\"not_eq\",\"gte\",\"lte\",\"between\"],\"sort_enabled\":true,\"search_enabled\":true},{\"field\":\"total_investors\",\"name\":\"并购方\",\"data_type\":\"collection\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"includes\",\"not_includes\",\"includes_all\"],\"sort_enabled\":false,\"search_enabled\":true},{\"field\":\"valuation\",\"name\":\"投后估值\",\"data_type\":\"amount\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"gte\",\"lte\",\"eq\",\"not_eq\",\"between\"],\"sort_enabled\":true,\"search_enabled\":true},{\"field\":\"report_title\",\"name\":\"相关报道\",\"data_type\":\"text\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"includes\",\"not_includes\",\"includes_all\"],\"sort_enabled\":false,\"search_enabled\":true},{\"field\":\"expose_date\",\"name\":\"曝光时间\",\"data_type\":\"date\",\"data_unit\":null,\"dict_type\":null,\"operation\":[\"gte\",\"lte\",\"eq\",\"not_eq\",\"between\"],\"sort_enabled\":true,\"search_enabled\":true}]","export_num":20,"type":"merger","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[{\"field\":\"id\",\"operation\":\"includes\",\"values\":[\"208455\",\"208399\",\"208314\",\"208277\",\"208345\",\"208206\",\"208305\",\"208018\",\"208149\",\"207956\",\"208183\",\"207921\",\"208155\",\"207954\",\"207941\",\"207929\",\"207757\",\"207938\",\"198516\",\"198388\"],\"type\":\"predicate\"}]","search":"[]"}
        r = requests.post(investment_export_url, data, headers=headers)
        if (r.status_code == 200):
            print('【并购本页导出成功】')
        else:
            print('【并购本页导出失败】')
        self.assertEqual(r.status_code, 200)

    def test_investment004(self):
        '''洞见数据—交易—上市列表'''
        investment_url = url + '/api/investment/search'
        data = {"curPage":1,"pageSize":20,"type":"ipo","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(investment_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        if r.status_code == 200:
            print('【洞见数据—交易—上市公司数量为：',x,'家】')
        else:
            print('【洞见数据—交易—上市列表获取失败】')
        self.assertGreaterEqual(x,7200) #原值8082→7997

    def test_investement004_exportNum(self):
        '''洞见数据—交易—上市—导出统计'''
        investment_export_num_url = url + '/api/investment/searchExportNum'
        data = {"type":"ipo","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[]","search":"[]"}
        r = requests.post(investment_export_num_url,data,headers = headers)
        d = r.json()
        print('【当前剩余导出条数：',d['data']['export_num'],'】')
        self.assertEqual(r.status_code,200)

    def test_investment005_time_asc(self):
        '''洞见数据—交易—上市—交易时间升序'''
        investment_url = url + '/api/investment/search'
        data = {"curPage":1,"pageSize":20,"type":"ipo","sort":"[{\"field\":\"finance_date\",\"sort\":\"asc\"}]","sub_search":"[]"}
        r = requests.post(investment_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        if r.status_code == 200 :
            print('【洞见数据—交易—上市公司有：',x,'家】')
        else:
            print('【洞见数据—交易—上市交易时间排序失败】')
        self.assertGreaterEqual(x,7200) #原值8082→7997

    def test_investment005(self):
        '''洞见数据—交易—上市后/定增'''
        investment_url = url + '/api/investment/search'
        data = {"curPage":1,"pageSize":20,"type":"after_ipo","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(investment_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【洞见数据—交易—上市后/定增公司有',x,'家】')
        self.assertGreaterEqual(x,4000)

    def test_investment005_dict(self):
        '''洞见数据—交易—上市后/定增轮次字典'''
        investment_dict_url = url + '/api/insight/dict_data?type=c_phase'
        r = requests.get(investment_dict_url,headers = headers)
        d = len(r.json()['data'])
        print('【洞见数据—交易—上市后/定增轮次字典内字段数量有：',d,'个】')
        self.assertEqual(d,22)

    def test_investment005_exportNum(self):
        '''洞见数据—交易—上市后/定增导出统计'''
        investment_exportNum_url = url + '/api/investment/searchExportNum'
        data = {"type":"after_ipo","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[]","search":"[]"}
        r = requests.post(investment_exportNum_url,data,headers = headers)
        d = r.json()['data']['export_num']
        print('【当前剩余导出条数为：',d,'条】')
        self.assertEqual(r.status_code,200)

    def test_investment005_time_desc(self):
        '''洞见数据—交易—上市后/定增—交易时间降序'''
        investment_url = url + '/api/investment/search'
        data = {"curPage":1,"pageSize":20,"type":"after_ipo","sort":"[{\"field\":\"finance_date\",\"sort\":\"desc\"}]","sub_search":"[]"}
        r = requests.post(investment_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【洞见数据—交易—上市后/定增公司有',x,'家】')
        self.assertGreaterEqual(x,4000)

    def test_organization(self):
        '''洞见数据—VC/PE'''
        organization_url = url + '/api/upgradefilter/getsearchdatabyobject'
        data = {"object":"organization","curPage":1,"pageSize":20,"data":"{\"sort\":[{\"field\":\"stat_rank.hot_score\",\"param\":[\"desc\"]}]}"}
        r = requests.post(organization_url,data,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【VP/PE检索结果有：',x,'家】')
        self.assertGreaterEqual(x,66000)

    # VC/PE检索示例
    def test_organization_example(self):
        organization_example_url = url + '/api/upgradefilter/getprefabricatedcondition?type=102'
        r = requests.get(organization_example_url,headers = headers)
        d = r.json()
        x1 = d['data'][0]['name']
        x2 = d['data'][1]['name']
        x3 = len(d['data'])
        print('【VC/PE的检索示例分别为：',x1,'、',x2,'】')
        self.assertEqual(x3,2)

# 有限合伙人

    # lp
    def test_lp(self):
        lp_url = url + '/api/lp?data={"condtion":[{"field":"lp_type","param":[]},{"field":"address","param":[]}],"sort":[{"field":"invested_amount","param":["desc"]}]}&curPage=1&pageSize=20&realTimeCount=1'
        r = requests.get(lp_url,headers = headers)
        d = r.json()
        x = d['data']['total']
        print('【有限合伙人数量有：',x,'家】')
        self.assertGreaterEqual(x,2800)

    # lp类型
    def test_lp_type(self):
        lp_type_url = url + '/api/dict?type=lp_type'
        r = requests.get(lp_type_url,headers = headers)
        d = r.json()
        x = len(d['data'])
        print('【lp 类型有：',x,'种】')
        self.assertEqual(x,13)

if __name__ == '__main__':
        unittest.main()
