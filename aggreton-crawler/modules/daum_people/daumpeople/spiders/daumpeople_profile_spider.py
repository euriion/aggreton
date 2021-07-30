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

# from scrapy.item import Item, Field
from daumpeople.items import DaumPeopleProfileItem
import chardet
import pprint
import copy
import re
import datetime
import time


class DaumPeopleProfileSpider(Spider):
    name = "daumpeople_profile"
    allowed_domains = ["search.daum.net"]
    start_urls = []

    def __init__(self, name=None, *args, **kwargs):
        super(DaumPeopleProfileSpider, self).__init__(*args, **kwargs)
        if name != None:
            self.start_urls.append("http://search.daum.net/search?w=tot&q=%s" % name)
        else:
            dz_mm = dz_model_manager.DzModelManager()
            names = dz_mm.get_all_names()
            total_entries = 0
            for name in names:
                self.start_urls.append("http://search.daum.net/search?w=tot&q=%s" % name.name)
                total_entries += 1
        log.msg("total %d start urls" % len(self.start_urls))

    def start_requests(self):
        requests = list(super(DaumPeopleProfileSpider, self).start_requests())
        for request in requests:
            request.cookies['captcha_pass'] = 'y'
            yield request

    def parse(self, response):
        selector = Selector(response)
        xpath_checkpoint = '//*[@id="profColl"]/div[1]/h2/text()' # 인물
        people_marker = selector.xpath(xpath_checkpoint)
        if people_marker != [] and people_marker.extract()[0].encode('utf-8') == '인물':  # there is an information about this name
            people_section = selector.xpath('//*[@id="profColl"]/div[2]/div/div[@class="info_basic"]/div[@class="wrap_cont"]')
            name_section = people_section[0].xpath('./div[@id="profCollPersonName"]')
            name = name_section.xpath("./strong/a/text()").extract()[0]

            d_movie_id = ""
            d_homodic_id = ""
            d_music_id = ""
            name_link_extraced = name_section.xpath("./strong/a/@href").extract()
            if name_link_extraced != []:
                name_link = name_link_extraced[0]
                movielink_extraced = re.findall(r'personId=([0-9]*)', name_link)
                homodiclink_extraced = re.findall(r'itemid=([0-9]*)', name_link)
                musiclink_extraced = re.findall(r'artistDetailId=([0-9]*)', name_link)
                if movielink_extraced != []:
                    d_movie_id = movielink_extraced[0]
                if homodiclink_extraced != []:
                    d_homodic_id = homodiclink_extraced[0]
                if musiclink_extraced != []:
                    d_music_id = musiclink_extraced[0]

            job = name_section.xpath("./span/text()").extract()[0]
            thumbnail_url = selector.xpath('//*[@id="profCollMain_img_0"]/a[1]/img/@src').extract()
            d_thumbnail_url = ""
            if thumbnail_url != []:
                d_thumbnail_url = thumbnail_url[0]

            birthday = None
            birthplace = ""
            zodiac_sign_chinese = ""
            zodiac_sign_star = ""

            birthday_title_extract = people_section.xpath('./dl[@class="collDl hlight_birth hlight_star"]/dt[@class="tit"]/text()')
            birthday_extracted = people_section.xpath('./dl[@class="collDl hlight_birth hlight_star"]/dd[@class="con"]/text()')
            if birthday_extracted != []:
                # if birthday_title_extract == "출생":
                birtyday_exracted = birthday_extracted[0].extract().split(',')
                birthday_set = re.findall(ur'([0-9]*?)년 ([0-9]*?)월 ([0-9]*?)일', birtyday_exracted[0])
                if birthday_set != []:
                    birthday = datetime.date(int(birthday_set[0][0]), int(birthday_set[0][1]), int(birthday_set[0][2]))
                # else:
                #     birtyday_exracted = birthday_extracted[0].extract().split(',')
                #     birthday_set = re.findall(ur'([0-9]*?)년 ([0-9]*?)월 ([0-9]*?)일', birtyday_exracted[0])
                #     print birthday_set
                #     birthday = datetime.date(int(birthday_set[0][0]), int(birthday_set[0][1]), int(birthday_set[0][2]))
                    if len(birtyday_exracted) >= 2:
                        birthplace = birtyday_exracted[1].strip()
                    if len(birthday_extracted) >= 2:
                        zodiac_set = birthday_extracted[1].extract().split(',')
                        zodiac_sign_chinese = zodiac_set[0].strip()
                        zodiac_sign_star = zodiac_set[1].strip()

            height = ""
            weight = ""
            blood_type = ""
            body_extracted = people_section.xpath('./dl[@class="collDl hlight_body"]/dd[@class="con"]/text()')
            if body_extracted != []:
                body_set = body_extracted
                # if len(body_set) >= 1:
                h_set = body_set.re(ur'([0-9]*)cm')
                w_set = body_set.re(ur'([0-9]*)kg')
                if h_set != []:
                    height = h_set[0].strip()
                if w_set != []:
                    weight = w_set[0].strip()
                bt_set = body_set.re(ur'([A-Z]*)형')
                if bt_set != []:
                    blood_type = bt_set[0][0]

            belong = ""
            belong_extracted = people_section.xpath('./dl[@class="collDl hlight_belong"]/dd[@class="con"]/a/text()').extract()
            if belong_extracted != []:
                belong = belong_extracted[0].strip()

            group = ""
            group_keys = ""
            group_extracted1 = people_section.xpath('./dl[@class="collDl hlight_group"]/dd[@class="con"]/*')
            if group_extracted1 != []:
                # group = group_extracted[0].strip()
                titles = group_extracted1.xpath('./text()').extract()
                links = group_extracted1.xpath('./@href').extract()
                pattern_ppkey = re.compile("&ppkey=([0-9]*)&")
                ppkeys = pattern_ppkey.findall(' '.join(links))
                group = ", ".join(titles)
                group_keys = ", ".join(ppkeys)

            debut_extracted = people_section.xpath('./dl[@class="collDl hlight_debut"]/dd[@class="con"]/text()')
            debut = ''
            if debut_extracted != []:
                debut = debut_extracted[0].extract().strip()

            site_extracted = people_section.xpath('./dl[@class="collDl hlight_site"]/dd[@class="con"]/*')
            site_official = ""
            site_youtube = ""
            site_twitter = ""
            site_fancafe = ""
            site_me2day = ""
            site_facebook = ""
            site_cyworld = ""
            if site_extracted != []:
                for site_selected in site_extracted:
                    site_category = site_selected.xpath("./text()").extract()[0]
                    site_url = site_selected.xpath("./@href").extract()[0]
                    if site_category.encode('utf8') == '공식사이트':
                        site_official = site_url
                    elif site_category.encode('utf8') == '유튜브':
                        site_youtube = site_url
                    elif site_category.encode('utf8') == '트위터':
                        site_twitter = site_url
                    elif site_category.encode('utf8') == '팬카페':
                        site_fancafe = site_url
                    elif site_category.encode('utf8') == '미투데이':
                        site_me2day = site_url
                    elif site_category.encode('utf8') == '페이스북':
                        site_facebook = site_url
                    elif site_category.encode('utf8') == '미니홈피':
                        site_cyworld = site_url

            members = ""
            member_list = []
            member_extracted = people_section.xpath('./dl[@class="collDl hlight_member"]/dd[@class="con"]/a[not(@id = "profileMemberLyr_btn")]')
            if member_extracted != []:
                # print member_extracted
                for member_selected in member_extracted:
                    member_set = member_selected.xpath("./text()").extract()
                    if len(member_set) >= 1:
                        member_list.append(member_set[0].encode('utf-8'))
                members = ", ".join(member_list)
            member_count = len(member_extracted)
            daum_people_profile_item = DaumPeopleProfileItem()
            # print "name: %s" % name
            # print "d_thumbnail_url: %s" % d_thumbnail_url
            # print "d_movie_id: %s" % d_movie_id
            # print "d_homodic_id: %s" % d_homodic_id
            # print "d_music_id: %s" % d_music_id
            # print "job: %s" % job
            # print "birthday: %s" % birthday
            # print "birthplace: %s" % birthplace
            # print "zodiac_sign_chinese: %s" % zodiac_sign_chinese
            # print "zodiac_sign_star: %s" % zodiac_sign_star
            # print "height: %s" % height
            # print "weight: %s" % weight
            # print "belong: %s" % belong
            # print "blood_type: %s" % blood_type
            # print "debut: %s" % debut
            # print "members: %s" % members
            # print "site_official: %s" % site_official
            # print "site_fancafe: %s" % site_fancafe
            # print "site_twitter: %s" % site_twitter
            # print "site_facebook: %s" % site_facebook
            # print "site_youtube: %s" % site_youtube
            # print "site_me2day: %s" % site_me2day
            # print "site_cyworld: %s" % site_cyworld

            daum_people_profile_item['name'] = name
            daum_people_profile_item['d_thumbnail_url'] = d_thumbnail_url
            daum_people_profile_item['d_movie_id'] = d_movie_id
            daum_people_profile_item['d_homodic_id'] = d_homodic_id
            daum_people_profile_item['d_music_id'] = d_music_id
            daum_people_profile_item['job'] = job
            daum_people_profile_item['birthday'] = birthday
            daum_people_profile_item['birthplace'] = birthplace
            daum_people_profile_item['zodiac_sign_chinese'] = zodiac_sign_chinese
            daum_people_profile_item['zodiac_sign_star'] = zodiac_sign_star
            daum_people_profile_item['height'] = height
            daum_people_profile_item['weight'] = weight
            daum_people_profile_item['belong'] = belong
            daum_people_profile_item['blood_type'] = blood_type
            daum_people_profile_item['debut'] = debut
            daum_people_profile_item['belong_group'] = group
            daum_people_profile_item['belong_group_keys'] = group_keys
            daum_people_profile_item['members'] = members
            daum_people_profile_item['member_count'] = member_count
            daum_people_profile_item['site_official'] = site_official
            daum_people_profile_item['site_fancafe'] = site_fancafe
            daum_people_profile_item['site_twitter'] = site_twitter
            daum_people_profile_item['site_facebook'] = site_facebook
            daum_people_profile_item['site_youtube'] = site_youtube
            daum_people_profile_item['site_me2day'] = site_me2day
            daum_people_profile_item['site_cyworld'] = site_cyworld
            daum_people_profile_item['image_urls'] = [d_thumbnail_url]
            return daum_people_profile_item
        else:
            return None
