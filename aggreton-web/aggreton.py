# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os


model_path = "%s/model" % os.environ['DZ_HOME']
sys.path.append(model_path)

from werkzeug.contrib.fixers import ProxyFix  # for Nginx
from flask import Flask, request, flash, render_template, render_template_string, url_for, send_file, send_from_directory, redirect
from sqlalchemy import desc, asc, or_, and_
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import Form, TextField, PasswordField, validators
from flask import g

import logging
import dz_models
import json
import hangul.translit
import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))

class DramazineConfiguration(object):
    def __init__(self):
        self.webapp_title = "DramaZine".decode('utf-8')
        self.webapp_sub_title = "- Korean TV series, Drama, K-POP, Entertainment"


# loading configuration
config = DramazineConfiguration()
page = {}

# application setting
app = Flask(__name__)
app.secret_key = 'SP2RPaUFqfCKkGn7oeYS'
#app.logger.setLevel(logging.WARNING)


# common environment variables
dz_home = os.environ['DZ_HOME']
db_conf = json.loads(open("%s/conf/db.conf" % dz_home).read())
mysql_connection_string = "%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=utf8" % db_conf
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://" + mysql_connection_string
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = dz_models.User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


# for auth
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(dz_models.User).filter_by(id=user_id).first()


@app.before_request
def before_request():
    g.user = current_user

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        page['title'] = 'DramaZine - Korean Entertainment Information'
        page['sub_title'] = ''.decode('utf-8')
        input=get_input(request)
        return render_template('login.html', config=config, page=page, input=input)
    username = request.form['username']
    password = request.form['password']
    registered_user = db.session.query(dz_models.User).filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    # return redirect(request.args.get('next') or url_for('main'))
    return redirect(url_for('top_actors'))

login_manager.login_view = 'login'

import urllib
from markupsafe import Markup


# fot Jinaj template
@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)


@app.template_filter('han2romanji')
def han2romanji(s):
    if len(s) == 2 or len(s) == 3:
        new_part1 = hangul.translit.romanize(s[0].encode("utf-8")).upper().replace("-", "")
        new_part2 = hangul.translit.romanize(s[1:].encode("utf-8"))
        if new_part1 == "I":
            new_part1 = "LEE"
        new_str = new_part1 + " " + new_part2
        return new_str
    else:
        new_str = hangul.translit.romanize(s.encode("utf-8"))
        return new_str[0].upper() + new_str[1:]


# for static
@app.route('/photo/<path:filename>')
def send_photo_image(filename):
    return send_from_directory("%s/data/crawled_images" % dz_home, filename)

def get_input(request):
    param = {}
    param['p'] = request.args.get('p', '')
    param['c'] = request.args.get('c', 'profile')

    return (param)


@app.route('/')
@app.route('/top_actors')
def top_actors():
    page['title'] = 'DramaZine - Korean Entertainment Information'
    page['sub_title'] = 'TOO 100 - Korean Actors, Actresses / 배우 / 韩国演员'.decode('utf-8')
    list_count = 100
    profile_records = db.session.query(dz_models.PeopleProfile).filter((dz_models.PeopleProfile.d_movie_id != '') & (dz_models.PeopleProfile.d_movie_id != None)
     & ((dz_models.PeopleProfile.job.like('%영화배우%')) | (dz_models.PeopleProfile.job.like('%탤렌트%')))).order_by(desc(dz_models.PeopleProfile.total_score)).limit(list_count)
    data = {'profile_records': profile_records}
    input = get_input(request)
    return render_template('top_actors.html', config=config, page=page, data=data, input=input)


@app.route('/top_beauties')
def top_beauties():
    page['title'] = 'DramaZine - Korean Entertainment Information'
    page['sub_title'] = 'TOO 100 - Korean Beauty People / 미인 / 韩国美人'.decode('utf-8')
    list_count = 100
    profile_records = db.session.query(dz_models.PeopleProfile).filter(dz_models.PeopleProfile.beauty_score > 0).order_by(desc(dz_models.PeopleProfile.beauty_score)).limit(list_count)
    data = {'profile_records': profile_records}
    input = get_input(request)
    return render_template('top_beauties.html', config=config, page=page, data=data, input=input)

@app.route('/top_singers')
def top_singers():
    page['title'] = 'DramaZine - Korean Entertainment Information'
    page['sub_title'] = 'TOO 100 - Korean Singers / 가수 / 韩国歌手'.decode('utf-8')
    list_count = 100
    profile_records = db.session.query(dz_models.PeopleProfile).filter((dz_models.PeopleProfile.d_music_id != '') & (dz_models.PeopleProfile.d_music_id != None)
     & ((dz_models.PeopleProfile.job.like('%가수%')))).order_by(desc(dz_models.PeopleProfile.total_score)).limit(list_count)
    data = {'profile_records': profile_records}
    input = get_input(request)
    return render_template('top_singers.html', config=config, page=page, data=data, input=input)


@app.route('/top_sportsstars')
def top_sportsstars():
    page['title'] = 'DramaZine - Korean Entertainment Information'
    page['sub_title'] = 'TOO 100 - Korean Sportsman / 스포츠스타 / 体育运动员'.decode('utf-8')
    list_count = 100
    profile_records = db.session.query(dz_models.PeopleProfile).filter((dz_models.PeopleProfile.d_homodic_id != '') & (dz_models.PeopleProfile.d_homodic_id != None)
     & ((dz_models.PeopleProfile.job.like('%선수%')))).order_by(desc(dz_models.PeopleProfile.total_score)).limit(list_count)
    data = {'profile_records': profile_records}
    input = get_input(request)
    return render_template('top_sportsstars.html', config=config, page=page, data=data, input=input)


@app.route('/admin_stats')
def admin_stats():
    page['title'] = 'DramaZine - Korean Entertainment Information'
    page['sub_title'] = 'Admin page'.decode('utf-8')
    data = {}
    people_name_count = db.session.query(dz_models.PeopleName).count()
    people_profile_count = db.session.query(dz_models.PeopleProfile).count()
    data['people_name_count'] = people_name_count
    data['people_profile_count'] = people_profile_count
    input=input
    return render_template('admin_stats.html', config=config, page=page, data=data, input=input)


@app.route('/celebrity')
def open_datasets():
    page['title'] = 'Korean Celebrities'
    page['sub_title'] = '한국유명인사'.decode('utf-8')
    records = []
    for raw_line in open("%s/data/opendataset_list.csv" % base_dir).readlines():
        line = raw_line.strip().decode('utf-8')
        fields = line.split('|')
        if len(fields) == 1:
            fields.append('')
        records.append(fields)
    return render_template('open_datasets.html', config=config, page=page, data=records)


@app.route('/search', methods=['GET'])
def search():
    page['title'] = 'Korean Celebrities'
    page['sub_title'] = '한국유명인사'.decode('utf-8')
    input=get_input(request)
    if request.method == 'POST':
        pass
    else:
        param = get_input(request)
        if param['c'] == 'profile':
            peopleprofile_records = None
            if param['p'] != '':
                try:
                    peopleprofile_records = db.session.query(dz_models.PeopleProfile).filter(dz_models.PeopleProfile.name == param['p']).all()
                except NoResultFound, e:
                    pass
            peoplename_records = None
            if param['p'] != '':
                try:
                    peoplename_records = db.session.query(dz_models.PeopleName).filter(dz_models.PeopleName.name == param['p']).all()
                except NoResultFound, e:
                    pass
            page['title'] = ''
            page['sub_title'] = ''
            data = {"profile_records":peopleprofile_records,"name_records":peoplename_records}
            return render_template('search_peopleprofile.html', config=config, page=page, data=data, input=param)
        else:
            page['title'] = 'Page not found'
            page['sub_title'] = ''
            return render_template('404.html', page=page, input=input), 404


@app.route('/super', methods=['GET', 'POST'])
@login_required
def super():
    page['title'] = 'DramaZine admin'
    page['sub_title'] = 'Admin'.decode('utf-8')
    input=get_input(request)
    return render_template('super.html', config=config, page=page, input=input)

@app.route('/super/people/scores/edit', methods=['GET', 'POST'])
@login_required
def super_people_scores_edit():
    page['title'] = 'Admin editorial - People scores'
    page['sub_title'] = ''
    input = get_input(request)
    if request.method == 'POST':

        if request.form.has_key('command') and request.form['command'] == 'beauty_score_apply':
            profile = db.session.query(dz_models.PeopleProfile).filter(dz_models.PeopleProfile.id == request.form['profile_id']).first()
            profile.beauty_score = int(request.form['beauty_score'])
            db.session.commit()

    if input['c'] == 'profile':
        peopleprofile_records = None
        if input['p'] != '':
            try:
                peopleprofile_records = db.session.query(dz_models.PeopleProfile).filter(dz_models.PeopleProfile.name == input['p']).all()
            except NoResultFound, e:
                pass
        peoplename_records = None
        if input['p'] != '':
            try:
                peoplename_records = db.session.query(dz_models.PeopleName).filter(dz_models.PeopleName.name == input['p']).all()
            except NoResultFound, e:
                pass
        page['title'] = ''
        page['sub_title'] = ''
        return render_template('super_people_scores_edit.html', config=config, page=page, data={"peopleprofile_records":peopleprofile_records,"peoplename_records":peoplename_records}, input=input)
    else:
        page['title'] = 'Page not found'
        page['sub_title'] = ''
        return render_template('404.html', page=page), 404

@app.route('/super/people/name/add', methods=['GET', 'POST'])
@login_required
def super_people_name_add():
    page['title'] = 'Admin editorial - people name add'
    page['sub_title'] = ''
    input = get_input(request)
    # input = request.form

    # if request.method == 'POST':
    exists = None
    if request.form.has_key('command') and request.form['command'] == 'add' and request.form['name'] != '':
        exists = db.session.query(dz_models.PeopleName).filter(dz_models.PeopleName.name == request.form['name']).count()
        if exists == 0:
            people_name = dz_models.PeopleName(request.form['name'])
            people_name.created = datetime.date.today()
            if request.form.has_key('daum'):
                people_name.daum = 'Y'
            else:
                people_name.daum = ''
            if request.form.has_key('naver'):
                people_name.naver = 'Y'
            else:
                people_name.naver = ''
            if request.form.has_key('joins'):
                people_name.joins = 'Y'
            else:
                people_name.joins = ''
            db.session.add(people_name)
            db.session.commit()
    return render_template('super_people_name_add.html', config=config, page=page, data={}, input=input, request=request, meta={'exists':exists})
    # else:
    #     page['title'] = 'Page not found'
    #     page['sub_title'] = ''
    #     return render_template('404.html', page=page, input=input), 404


@app.errorhandler(404)
def page_not_found(e):
    page['title'] = 'Page not found'
    page['sub_title'] = ''
    input = get_input(request)
    return render_template('404.html', page=page, input=input), 404

if __name__ == '__main__':
    if len(sys.argv) != 1 and sys.argv[1] == "dev":
        print("Staring webapp as Development mode")
        app.run(host='0.0.0.0', port=38080, debug=True)
    if len(sys.argv) == 1 or sys.argv[1] != "dev":
        # app.run(host='0.0.0.0', port=80, debug=True)
        print("Staring webapp as Production mode")

        @werkzeug.serving.run_with_reloader
        def runServer():
            app.debug = True
            app.jinja_options["TEMPLATES_AUTO_RELOAD"] = True
            ws = gevent.wsgi.WSGIServer(('0.0.0.0', 30080), app, use_reloader=True)
            ws.serve_forever()
            # if len(sys.argv) == 1 or sys.argv[1] != "dev":
            #   app.wsgi_app = ProxyFix(app.wsgi_app)
            #   app.run(host='0.0.0.0', port=30080, debug=True)
