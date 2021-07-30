# -*- coding: utf-8 -*-
import os
import sys
import json
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker
import MySQLdb
import datetime
sa_base = declarative_base()
# sa_metadata = MetaData()


class User(sa_base):
    __tablename__ = "user"
    id = sa.Column('id', sa.Integer, primary_key=True)
    username = sa.Column('username', sa.String(20), unique=True, index=True)
    password = sa.Column('password', sa.String(12))
    email = sa.Column('email', sa.String(50), unique=True, index=True)
    nickname = sa.Column('nickname', sa.String(30), unique=False, index=True)
    is_super = sa.Column('is_super', sa.String(1), unique=False, index=True)
    registered_on = sa.Column('registered_on', sa.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def is_super(self):
        if self.is_super.upper() == 'Y':
            return True
        else:
            return False

    def __repr__(self):
        return '<User %r>' % (self.username)

class PeopleName(sa_base):
    __tablename__ = 'people_name'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Unicode(100, collation='utf8'), unique=True)
    english_name = sa.Column(sa.String(100), unique=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Name: '%r'>" % self.name.encode(sys.stdout.encoding)

class PeopleProfile(sa_base):
    __tablename__ = 'people_profile'
    id = sa.Column(sa.Integer, sa.Sequence('people_id_seq'), primary_key=True, unique=True)
    name = sa.Column(sa.Unicode(80))
    d_thumbnail_url = sa.Column(sa.String(300))
    thumbnail_filename = sa.Column(sa.String(100))
    job = sa.Column(sa.Unicode(100))
    gender = sa.Column(sa.String(1))
    legal_name = sa.Column(sa.Unicode(80))
    english_name = sa.Column(sa.Unicode(80))
    chinese_name = sa.Column(sa.Unicode(80))
    site_official = sa.Column(sa.String(200))
    site_twitter = sa.Column(sa.String(200))
    site_facebook = sa.Column(sa.String(200))
    site_cyworld = sa.Column(sa.String(200))
    site_me2day = sa.Column(sa.String(200))
    site_youtube = sa.Column(sa.String(200))
    site_fancafe = sa.Column(sa.String(200))
    birthday = sa.Column(sa.Date())
    birthplace = sa.Column(sa.Unicode(100))
    deathday = sa.Column(sa.Date())
    age = sa.Column(sa.Integer())
    weight = sa.Column(sa.Integer())
    height = sa.Column(sa.Integer())
    debut = sa.Column(sa.Unicode(100))
    debut_year = sa.Column(sa.Integer())
    belong_id = sa.Column(sa.String(50))
    belong = sa.Column(sa.Unicode(100))
    zodiac_sign_chinese = sa.Column(sa.Unicode(30))
    zodiac_sign_star = sa.Column(sa.Unicode(30))
    blood_type = sa.Column(sa.String(1))
    members = sa.Column(sa.Unicode(200))
    member_count = sa.Column(sa.Integer())
    belong_group = sa.Column(sa.Unicode(200))
    d_movie_id = sa.Column(sa.String(20))
    d_homodic_id = sa.Column(sa.String(20))
    d_music_id = sa.Column(sa.String(20))
    total_score = sa.Column(sa.Integer())
    beauty_score = sa.Column(sa.Integer())
    handsome_score = sa.Column(sa.Integer())
    sexy_score = sa.Column(sa.Integer())
    dandy_score = sa.Column(sa.Integer())
    goodness_score = sa.Column(sa.Integer())
    badness_score = sa.Column(sa.Integer())
    created = sa.Column(sa.TIMESTAMP)
    modified = sa.Column(sa.TIMESTAMP, onupdate=sa.text('current_timestamp'))

    def __init__(self):
        pass

    def __repr__(self):
        return '<People %r>' % self.name.encode(sys.stdout.encoding)

if __name__ == '__main__':
    dz_home = os.environ['DZ_HOME']
    db_conf = json.loads(open("%s/conf/db.conf" % dz_home).read())
    mysql_connection_string = "%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=utf8" % db_conf
    sa_engine = create_engine("mysql+mysqldb://%s" % mysql_connection_string, encoding="utf8")
    # sa_metadata.bind = sa_engine
    # sa_metadata.reflect()
    # for tbl in sa_metadata.tables:
    #     print tbl
    # sa_engine.execute(tbl_name.delete())
    # sa_connection = sa_engine.connect()
    Session = sessionmaker(bind=sa_engine)
    # Session.configure(bind=sa_engine)
    session = Session()




