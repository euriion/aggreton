# -*- coding: utf-8 -*-
__author__ = 'euriion'
import os
import sys
import json
import sqlalchemy
from dz_models import *

class DzModelManager(object):
    _db_conf = None
    _db_connect_string = None
    _sa_engine = None
    _db_session = None
    # _sa_metadata = None
    _sa_base = None
    _tables = {}

    def __init__(self):
        dz_home = os.environ['DZ_HOME']
        self._db_conf = json.loads(open("%s/conf/db.conf" % dz_home).read())
        #$?charset=utf8
        self._db_connect_string = "%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=utf8" % self._db_conf
        self._sa_engine = sqlalchemy.create_engine("mysql+mysqldb://%s" % self._db_connect_string, encoding="utf8")
        self._sa_base = sa_base
        #self._sa_base.metadata.reflect(self._sa_engine)

        # self._sa_metadata.bind = self._sa_engine

        # self._tables['name'] = Name
        # self._tables['people'] = People
        # self._tables['name'].metadata = self._sa_metadata
        # self._tables['people'].metadata = self._sa_metadata

        # self._sa_metadata.reflect()
        # sa_engine.execute(tbl_name.delete())
        # sa_connection = sa_engine.connect()
        Session = sqlalchemy.orm.sessionmaker(bind=self._sa_engine)
        # Session.configure(bind=sa_engine)
        self._db_session = Session()


    def create_tables(self):
        #db_engine = dz_model.sa.create_engine(self.db_uri, echo=True)
        #dz_model.Base.metadata.create_all(db_engine)
        self._sa_base.metadata.create_all(self._sa_engine)

    def append_people(self):
        pass

    def append_names(self):
        name_list = open("%s/crawl/seeds/daum_people_names.csv" % os.environ['DZ_HOME']).readlines()
        name_list.extend(open("%s/crawl/seeds/daum_people_names.new.csv" % os.environ['DZ_HOME']).readlines())
        for raw_line in name_list:
            new_name = raw_line.strip().decode('utf-8')
            exist_name = self._db_session.query(PeopleName).filter_by(name=new_name.encode('utf-8')).first()
            if exist_name == None:
                new_name = PeopleName(new_name)
                self._db_session.add(new_name)
            else:
                print "%s is exist" % new_name
        self._db_session.commit()

    def get_all_names(self):
        results = self._db_session.query(PeopleName).order_by(PeopleName.name)
        self._db_session.close()
        return results

    def get_all_profiles(self):
        results = self._db_session.query(PeopleProfile).all()
        self._db_session.close()
        return results



if __name__ == '__main__':
    model_manager = DzModelManager()
    # model_manager.append_names()
    model_manager.create_tables()
