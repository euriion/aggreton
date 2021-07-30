# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
import json
import datetime
from scrapy.exceptions import DropItem

# model_path = "%s/model" % os.environ['DZ_HOME']
# sys.path.append(model_path)
#
# import sqlalchemy
# import sqlalchemy.orm
# import dz_models

class DaumKeywordPvPipeline(object):
    def __init__(self):
        pass
        # dz_home = os.environ['DZ_HOME']
        # db_conf = json.loads(open("%s/config/db.conf" % dz_home).read())
        # db_connect_string = "%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=utf8" % db_conf
        # sa_engine = sqlalchemy.create_engine("mysql+mysqldb://%s" % db_connect_string, encoding="utf8")
        # sa_base = dz_models.sa_base
        # self.dbSession = sqlalchemy.orm.sessionmaker(bind=sa_engine)
        # #self.db_session = Session()

    def open_spider(self, spider):
        print "----- [%s] spider open: %s" % (self.__class__.__name__, spider.name)

    def close_spider(self, spider):
        print "----- [%s] spider close: %s" % (self.__class__.__name__, spider.name)

    def process_item(self, item, spider):
        if spider.name == 'daumkeyword_spider' and item != None:
            print item
            # session = self.dbSession()
            is_new = False
            # name_count = session.query(dz_models.PeopleProfile).filter_by(name=item['name']).count()

            # people_profile = None
            # if name_count == 0:
            #     pass
            #     # is_new = True
            #     # people_profile = dz_models.PeopleProfile()
            #     # people_name.created = datetime.date.today()
            #     session.close()
            #     return None
            # else:
            #
            #     is_new = False
            #     people_profiles = session.query(dz_models.PeopleProfile).filter_by(name=item['name']).all()
            #     for people_profile in people_profiles:
            #         people_profile.total_score = item['month_1']
            #         session.commit()
            #         print "%s total_score: %s" % (item['name'], people_profile.total_score)
            #     session.close()
            #     return item

            # # people.id = ''
            # people_name.name = item['name']
            # people_name.daum = 'Y'
            # try:
            #     if is_new:
            #         session.add(people_name)
            #         session.commit()
            # except:
            #     session.rollback()
            #     raise
            # finally:
            #     session.close()
            # return item
        else:
            return item


class FinalPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        # print "----- [%s] spider open: %s" % (self.__class__.__name__, spider.name)
        pass

    def close_spider(self, spider):
        # print "----- [%s] spider close: %s" % (self.__class__.__name__, spider.name)
        pass

    def process_item(self, item, spider):
        # print "----- [%s] pipeline process" % self.__class__.__name__
        if spider.name == 'daumpeopleprofile' and item != None:
            return item
        else:
            return item
