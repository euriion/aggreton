# -*- coding: utf-8 -*-
import os
import sys

# sys.path.append("%s/model" % os.environ['DZ_HOME'])
# import dz_model_manager

import urllib
import urllib2
from scrapy.spider import Spider
from scrapy.spider import Request
from scrapy.spider import log
from scrapy.selector import Selector
from scrapy.http import FormRequest
from scrapy.item import Item, Field
from items import DaumKeywordItem
import chardet
import pprint

import copy
import random
import string
import json
import re


class DaumKeywordPvSpider(Spider):
    name = "daumkeyword_pv"
    allowed_domains = ["http://adnetworks.biz.daum.net/"]
    _search_name = None

    def __init__(self, person_name=None, *args, **kwargs):
        super(DaumKeywordPvSpider, self).__init__(*args, **kwargs)
        self.person_name = person_name


    def start_requests(self):
        # requests = list(super(DaumKeywordPvSpider, self).start_requests())
        # for request in requests:
        #     request.cookies['captcha_pass'] = 'y'
        #     yield request

        if self.person_name != None:
            scriptSessionId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(46))
            request = FormRequest(
                        url="http://adnetworks.biz.daum.net/dwr/call/plaincall/KwordDwrService.getChartData.dwr",
                        formdata={
                            'callCount':'1',
                            'windowName':'',
                            'c0-scriptName':'KwordDwrService',
                            'c0-methodName':'getChartData',
                            'c0-id':'0',
                            'c0-param0': 'string:%s' % self.person_name,
                            'batchId':'3',
                            'instanceId':'0',
                            'page':'%2Finsight%2Ftrend.jsp',
                            # 'scriptSessionId':'6wa7JwcMt2SIxQ0VmErYkUYtHnk/Y1oZHnk-JdNRS51ak'
                            'scriptSessionId':scriptSessionId
                        })
            request.meta['name'] = self.person_name
            yield request
        else:
            dz_mm = dz_model_manager.DzModelManager()
            people_profiles = dz_mm.get_all_profiles()
            total_entries = 0
            for people_profile in people_profiles:
                scriptSessionId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(46))
                # self.start_urls.append("http://search.daum.net/search?w=tot&q=%s" % people_name.name)
                total_entries += 1
                print people_profile.name
                request = FormRequest(
                        url="http://adnetworks.biz.daum.net/dwr/call/plaincall/KwordDwrService.getChartData.dwr",
                        formdata={
                            'callCount':'1',
                            'windowName':'',
                            'c0-scriptName':'KwordDwrService',
                            'c0-methodName':'getChartData',
                            'c0-id':'0',
                            'c0-param0': 'string:%s' % people_profile.name,
                            'batchId':'3',
                            'instanceId':'0',
                            'page':'%2Finsight%2Ftrend.jsp',
                            'scriptSessionId':scriptSessionId
                        })
                request.meta['name'] = people_profile.name
                yield request

    def parse(self, response):
        # print "====================================================="
        # print response.body
        # print "====================================================="
        # original content line
        # r.handleCallback("3","0",{GenderCount:{FEMALE:31,MALE:69},MonthViewCount:{"LABEL_2":"2014.03","LABEL_1":"2014.04","LABEL_8":"2013.09","LABEL_7":"2013.10","LABEL_9":"2013.08","LABEL_4":"2014.01","LABEL_3":"2014.02","LABEL_6":"2013.11","LABEL_5":"2013.12","MONTH_9":164843,"MONTH_8":326938,"MONTH_7":174617,"MONTH_6":79222,"MONTH_5":40682,"MONTH_4":62588,"MONTH_3":52671,"MONTH_2":37058,"MONTH_1":118754},AgeCount:{"AGE_30":36,"AGE_20":21,"AGE_UNDER10":2,"AGE_50":15,"AGE_40":24,"AGE_10":3}});
# })();

        selector = Selector(response)
        json_content = selector.re(r'r[.]handleCallback\("3","0",(.*)\)')


        if len(json_content) > 0:
            data_content = json_content[0]
            data_content = data_content.replace('GenderCount:', '"GenderCount":')
            data_content = data_content.replace('FEMALE:', '"FEMALE":')
            data_content = data_content.replace('MALE:', '"MALE":')
            data_content = data_content.replace('MonthViewCount:', '"MonthViewCount":')
            data_content = data_content.replace('AgeCount:', '"AgeCount":')
            data = json.loads(data_content)


            daumkeyword_pv_item = DaumKeywordPvItem()
            daumkeyword_pv_item['name'] = response.meta['name']
            daumkeyword_pv_item['female'] = data['GenderCount']['FEMALE']
            daumkeyword_pv_item['male'] = data['GenderCount']['MALE']
            daumkeyword_pv_item['age_10'] = data['AgeCount']['AGE_10']
            daumkeyword_pv_item['age_20'] = data['AgeCount']['AGE_20']
            daumkeyword_pv_item['age_30'] = data['AgeCount']['AGE_30']
            daumkeyword_pv_item['age_40'] = data['AgeCount']['AGE_40']
            daumkeyword_pv_item['age_50'] = data['AgeCount']['AGE_50']
            daumkeyword_pv_item['age_00'] = data['AgeCount']['AGE_UNDER10']
            daumkeyword_pv_item['label_1'] = data['MonthViewCount']['LABEL_1']
            daumkeyword_pv_item['label_2'] = data['MonthViewCount']['LABEL_2']
            daumkeyword_pv_item['label_3'] = data['MonthViewCount']['LABEL_3']
            daumkeyword_pv_item['label_4'] = data['MonthViewCount']['LABEL_4']
            daumkeyword_pv_item['label_5'] = data['MonthViewCount']['LABEL_5']
            daumkeyword_pv_item['label_6'] = data['MonthViewCount']['LABEL_6']
            daumkeyword_pv_item['label_7'] = data['MonthViewCount']['LABEL_7']
            daumkeyword_pv_item['label_8'] = data['MonthViewCount']['LABEL_8']
            daumkeyword_pv_item['label_9'] = data['MonthViewCount']['LABEL_9']
            daumkeyword_pv_item['month_1'] = data['MonthViewCount']['MONTH_1']
            daumkeyword_pv_item['month_2'] = data['MonthViewCount']['MONTH_2']
            daumkeyword_pv_item['month_3'] = data['MonthViewCount']['MONTH_3']
            daumkeyword_pv_item['month_4'] = data['MonthViewCount']['MONTH_4']
            daumkeyword_pv_item['month_5'] = data['MonthViewCount']['MONTH_5']
            daumkeyword_pv_item['month_6'] = data['MonthViewCount']['MONTH_6']
            daumkeyword_pv_item['month_7'] = data['MonthViewCount']['MONTH_7']
            daumkeyword_pv_item['month_8'] = data['MonthViewCount']['MONTH_8']
            daumkeyword_pv_item['month_9'] = data['MonthViewCount']['MONTH_9']
            return daumkeyword_pv_item
        else:
            return None

