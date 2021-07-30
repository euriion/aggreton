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

model_path = "%s/model" % os.environ['DZ_HOME']
sys.path.append(model_path)

import sqlalchemy
import sqlalchemy.orm
import dz_models

class NameWriterPipeline(object):

    def __init__(self):
        self.name_file = open("../seeds/daum_people_names.new.csv", 'w')

    def process_item(self, item, spider):
        if item['name'] != None:
            line = "%s\n" % item['name']
            self.name_file.write(line.encode('utf-8'))
            return item
        else:
            raise DropItem("empty name: %s" % item)


class DeduplicatePeopleNamePipeline(object):
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        if spider.name != 'daumpeople_name':
            return item
        else:
            if item['name'] in self.names_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.names_seen.add(item['name'])
                return item

class DaumPeopleProfilePipeline(object):
    def __init__(self):
        dz_home = os.environ['DZ_HOME']
        db_conf = json.loads(open("%s/config/db.conf" % dz_home).read())
        db_connect_string = "%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=utf8" % db_conf
        sa_engine = sqlalchemy.create_engine("mysql+mysqldb://%s" % db_connect_string, encoding="utf8")
        sa_base = dz_models.sa_base
        self.dbSession = sqlalchemy.orm.sessionmaker(bind=sa_engine)
        #self.db_session = Session()

    def open_spider(self, spider):
        print "----- [%s] spider open: %s" % (self.__class__.__name__, spider.name)

    def close_spider(self, spider):
        print "----- [%s] spider close: %s" % (self.__class__.__name__, spider.name)

    def process_item(self, item, spider):
        # print "----- [%s] pipeline process" % self.__class__.__name__
        if spider.name == 'daumpeople_profile' and item != None:
            session = self.dbSession()
            is_new = False
            name_count = session.query(dz_models.PeopleProfile).filter_by(name=item['name']).count()

            # people = dz_model.People(**item)
            people = None
            if name_count == 0:
                is_new = True
                people = dz_models.PeopleProfile()
                people.created = datetime.date.today()
            else:
                is_new = False
                people = session.query(dz_models.PeopleProfile).filter_by(name=item['name']).one()

            # people.id = ''
            people.name = item['name']
            people.job = item['job']
            # people.gender = item['gender']
            # people.legal_name = item['legal_name']
            # people.english_name = item['english_name']
            # people.chinese_name = item['chinese_name']
            people.site_official = item['site_official']
            people.site_twitter = item['site_twitter']
            people.site_facebook = item['site_facebook']
            people.site_cyworld = item['site_cyworld']
            people.site_me2day = item['site_me2day']
            people.site_youtube = item['site_youtube']
            people.site_fancafe = item['site_fancafe']
            people.birthday = item['birthday']
            people.birthplace = item['birthplace']
            # people.deathday = item['deathday']
            # people.age = item['age']
            people.weight = item['weight']
            people.height = item['height']
            people.debut = item['debut']
            # people.debut_year = item['debut_year']
            # people.belong_id = item['belong_id']
            people.belong = item['belong']
            people.zodiac_sign_chinese = item['zodiac_sign_chinese']
            people.zodiac_sign_star = item['zodiac_sign_star']
            people.blood_type = item['blood_type']
            people.members = item['members']
            people.belong_group = item['belong_group']
            # people.belong_group_keys = item['belong_group_keys']
            people.d_movie_id = item['d_movie_id']
            people.d_homodic_id = item['d_homodic_id']
            people.d_music_id = item['d_music_id']
            people.d_thumbnail_url = item['d_thumbnail_url']
            # people.last_updated = item['last_updated']
            # people.image_urls = item['image_urls']
            # people.images = item['images']
            people.thumbnail_filename = item['images'][0]['path']

            for group_name in people.belong_group.split(", "):
                if session.query(dz_models.PeopleName).filter_by(name=group_name).count() == 0:
                    people_name = dz_models.PeopleName(group_name)
                    people_name.daum = 'Y'
                    session.add(people_name)
            for member_name in people.members.split(", "):
                if session.query(dz_models.PeopleName).filter_by(name=member_name).count() == 0:
                    people_name = dz_models.PeopleName(member_name)
                    people_name.daum = 'Y'
                    session.add(people_name)
            try:
                if is_new:
                    session.add(people)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            return item
        else:
            return item

class DaumPeopleNamePipeline(object):
    def __init__(self):
        dz_home = os.environ['DZ_HOME']
        db_conf = json.loads(open("%s/config/db.conf" % dz_home).read())
        db_connect_string = "%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=utf8" % db_conf
        sa_engine = sqlalchemy.create_engine("mysql+mysqldb://%s" % db_connect_string, encoding="utf8")
        sa_base = dz_models.sa_base
        self.dbSession = sqlalchemy.orm.sessionmaker(bind=sa_engine)
        #self.db_session = Session()

    def open_spider(self, spider):
        print "----- [%s] spider open: %s" % (self.__class__.__name__, spider.name)

    def close_spider(self, spider):
        print "----- [%s] spider close: %s" % (self.__class__.__name__, spider.name)

    def process_item(self, item, spider):
        # print "----- [%s] pipeline process" % self.__class__.__name__
        if spider.name == 'daumpeople_name' and item != None:
            session = self.dbSession()
            is_new = False
            name_count = session.query(dz_models.PeopleName).filter_by(name=item['name']).count()

            # people = dz_model.People(**item)
            people_name = None
            if name_count == 0:
                is_new = True
                people_name = dz_models.PeopleName()
                people_name.created = datetime.date.today()
            else:
                is_new = False
                people_name = session.query(dz_models.PeopleName).filter_by(name=item['name']).one()
                print "%s exists" % item['name']

            # people.id = ''
            people_name.name = item['name']
            people_name.daum = 'Y'
            try:
                if is_new:
                    session.add(people_name)
                    session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            return item
        else:
            return item


class DaumKeywordPvPipeline(object):
    def __init__(self):
        dz_home = os.environ['DZ_HOME']
        db_conf = json.loads(open("%s/config/db.conf" % dz_home).read())
        db_connect_string = "%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=utf8" % db_conf
        sa_engine = sqlalchemy.create_engine("mysql+mysqldb://%s" % db_connect_string, encoding="utf8")
        sa_base = dz_models.sa_base
        self.dbSession = sqlalchemy.orm.sessionmaker(bind=sa_engine)
        #self.db_session = Session()

    def open_spider(self, spider):
        print "----- [%s] spider open: %s" % (self.__class__.__name__, spider.name)

    def close_spider(self, spider):
        print "----- [%s] spider close: %s" % (self.__class__.__name__, spider.name)

    def process_item(self, item, spider):
        if spider.name == 'daumkeyword_pv' and item != None:
            # print item
            session = self.dbSession()
            is_new = False
            name_count = session.query(dz_models.PeopleProfile).filter_by(name=item['name']).count()

            people_profile = None
            if name_count == 0:
                pass
                # is_new = True
                # people_profile = dz_models.PeopleProfile()
                # people_name.created = datetime.date.today()
                session.close()
                return None
            else:

                is_new = False
                people_profiles = session.query(dz_models.PeopleProfile).filter_by(name=item['name']).all()
                for people_profile in people_profiles:
                    people_profile.total_score = item['month_1']
                    session.commit()
                    print "%s total_score: %s" % (item['name'], people_profile.total_score)
                session.close()
                return item

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