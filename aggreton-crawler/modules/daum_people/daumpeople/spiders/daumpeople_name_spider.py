# -*- coding: utf-8 -*-
import os
import sys

sys.path.append("%s/model" % os.environ['DZ_HOME'])
import dz_model_manager

import urllib
import urllib2
from scrapy.spider import Spider
from scrapy.spider import Request
from scrapy.spider import log
from scrapy.selector import Selector
from scrapy.item import Item, Field
from daumpeople.items import DaumPeopleNameItem
import chardet
import pprint

import copy


class DaumPeopleNameSpider(Spider):
    name = "daumpeople_name"
    allowed_domains = ["search.daum.net"]

    def __init__(self, name=None, *args, **kwargs):
        super(DaumPeopleNameSpider, self).__init__(*args, **kwargs)
        if name != None:
            self.start_urls.append("http://search.daum.net/search?w=tot&q=%s" % name)
        else:
            dz_mm = dz_model_manager.DzModelManager()
            people_names = dz_mm.get_all_names()
            total_entries = 0
            for people_name in people_names:
                self.start_urls.append("http://search.daum.net/search?w=tot&q=%s" % people_name.name)
                total_entries += 1
        log.msg("total %d start urls" % len(self.start_urls))
        # if os.path.exists(self.seed_names_filename):
        #     seed_file = open(self.seed_names_filename)
        #     for name in seed_file.readlines():
        #         name = name.strip().decode('utf-8')
        #         if name == '':
        #             continue
        #         target_url = "http://search.daum.net/search?w=tot&rtmaxcoll=PRF&q=%s" % name
        #         if self.seed_names.has_key(name):
        #             self.seed_names[name] += 1
        #         else:
        #             self.seed_names[name] = 1
        #     seed_file.close()
        # else:
        #     log.msg("seed file does not exists: %s" % self.seed_names_filename)

        # if os.path.exists(self.seed_names_filename_new):
        #     seed_file2 = open(self.seed_names_filename_new)
        #     for name in seed_file2.readlines():
        #         name = name.strip().decode('utf-8')
        #         if name == '':
        #             continue
        #         if self.seed_names.has_key(name):
        #             self.seed_names[name] += 1
        #         else:
        #             self.seed_names[name] = 1
        #     seed_file2.close()
        # else:
        #     log.msg("seed file does not exists: %s" % self.seed_names_filename_new)
        #
        # seed_file = open(self.seed_names_filename, 'w')
        # seed_file.write("\n".join(self.seed_names.keys()).encode('utf-8') + "\n")
        # seed_file.close()


    def start_requests(self):
        # requests = list(super(DaumPeopleNameSpider, self).start_requests())
        # for name in self.seed_names.keys():
        #     # target_url = "http://search.daum.net/search?nil_suggest=btn&nil_ch=&rtupcoll=&w=tot&m=&f=&lpp=&DA=SBCO&sug=&sq=&o=&sugo=&q=%s" % name
        #     request = Request(target_url)
        #     request.cookies['captcha_pass'] = 'y'
        #     request.meta['_name'] = name
        #     requests.append(request)
        # return requests
        requests = list(super(DaumPeopleNameSpider, self).start_requests())
        for request in requests:
            request.cookies['captcha_pass'] = 'y'
            yield request


    def parse(self, response):
        selector = Selector(response)
        xpath_list = (
            '//*[@id="profCollCont8"]/div[1]/div/ul/li',  # 베스트 연관
            '//*[@id="profCollCont8"]/div[3]/div/ul/li',  # 같은 소속
            '//*[@id="profCollCont8"]/div[4]/div/ul/li',  # 함께 작업한
            '//*[@id="profCollCont8"]/div[7]/div/ul/li',  # 같은 학교
            # '//*[@id="profCollCont8"]/div[2]/div[1]/ul/li',     # 가족
            '//*[@id="profCollCont8"]/div[8]/div[1]/ul/li'  # 같은 지역 출신
        )

        checkpoint = selector.xpath('//*[@id="profColl"]/div[1]/h2')  # 인물탭확인

        if checkpoint == []:  # there is no information about people
            pass
        else:
            for xpath_item in xpath_list:
                rel_peoples = selector.xpath(xpath_item)
                for rel_person in rel_peoples:
                    name_xpath_items = rel_person.xpath("div[2]/em/a/@href").extract()
                    if name_xpath_items != []:
                        href_content = name_xpath_items[0]
                        href_content = href_content.encode('utf8')
                        new_name = href_content.split('&')[1].split('=')[1]
                        new_name = urllib.unquote(new_name).decode('utf8')
                        log.msg("name found: %s" % new_name)
                        people_name_item = DaumPeopleNameItem()
                        people_name_item['name'] = new_name
                        yield people_name_item
        # if names.has_key(new_name):
        #     names[new_name] += 1
        # else:
        #     names[new_name] = 1
        # for name in names.keys():
        #     if not name in self.seed_names:
        #         name_item = NameItem()
        #         name_item['name'] = name
        #         yield name_item

