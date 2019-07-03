#!/usr/bin/python3
import requests
from flask import render_template, redirect, url_for, flash, jsonify, request, session
from flaskRegister import app, db, AMAP_KEY
from flaskRegister.models import OzingSalesmanUser, Province, City, District
from flaskRegister.forms import SalesmanForm


@app.route('/', methods=['GET', 'POST'])
def register():
    form = SalesmanForm()
    if form.validate_on_submit():
        session['legend'] = '注册成功，欢迎您'
        province_id = form.province.data
        province = Province.query.get(province_id).name
        city_id = form.city.data
        city = City.query.get(city_id).name
        district_id = form.district.data
        district = District.query.get(district_id).name
        endpoint = form.endpoint.data
        name = form.name.data
        phonenumber = form.phonenumber.data
        gender_id = form.gender.data
        gender = '女' if gender_id == '1' else '男'
        weichat_id = form.weichat_id.data
        salesman = OzingSalesmanUser(province=province, city=city, district=district, endpoint=endpoint, \
                                     salesman_phone=phonenumber, salesman_name=name, sex=gender, wx_id=weichat_id)
        db.session.add(salesman)
        db.session.commit()
        return redirect(url_for('register'))
    if session.get('legend') is not None:
        legend = session.get('legend')
    else:
        legend = '欢迎注册'

    if legend == '注册成功，欢迎您':
        s = OzingSalesmanUser.query.filter_by(salesman_phone=session['phone']).first()
        if s is not None:
            form.province.choices = [(10000, s.province)]
            form.city.choices = [(10000, s.city)]
            form.district.choices = [(10000, s.district)]
            form.endpoint.data = s.endpoint
            form.name.data = s.salesman_name
            form.phonenumber.data = s.salesman_phone
            form.gender.choices = [(10000, s.sex)]
            if s.wx_id == '':
                form.weichat_id.data = ' '
            else:
                form.weichat_id.data = s.wx_id
        session['phone'] = None
        session['valid_code'] = None
        session['legend'] = None
    return render_template('new.html', legend=legend, form=form)

        #return render_template('registerconfirm.html')


@app.route('/provinces/', methods=['GET'])
def provinces():
    provinces = [{'id': 0, 'name': '请选择省'}]
    province_all = Province.query.all()
    for province in province_all:
        provinces.append({'id': province.id, 'name': province.name})
    return jsonify(provinces)


@app.route('/regions/', methods=['GET'])
def regions():
    province_id = request.args.get('province')
    city_id = request.args.get('city')
    if province_id is not None:
        cities = [{'id': 0, 'name': '请选择市'}]
        p = Province.query.get(province_id)
        for city in p.cities:
            cities.append({'id': city.id, 'name': city.name})
        return jsonify(cities)

    if city_id is not None:
        districts = [{'id': 0, 'name': '请选择区/县'}]
        c = City.query.get(city_id)
        for district in c.districts:
            districts.append({'id': district.id, 'name': district.name})
        return jsonify(districts)


@app.route('/validcode/')
def validcode():
    phone = request.args.get('phone')
    salesman = OzingSalesmanUser.query.filter_by(salesman_phone=phone).first()
    if salesman is not None:
        return jsonify({'code': 1001})  # 1001 phone is occupied
    else:
        session['phone'] = phone
    payload = {'mobile': phone, 'type': 'register'}
    r = requests.post('http://boss.hjx.com/ozing/timer/user/fetchAuthCode', data=payload)
    result = r.json()
    print('')
    if result['status'] == 100:
        valid_code = result['jsessionid']
        #print('validcode@@@@{}'.format(valid_code))
        session['valid_code'] = valid_code
        return jsonify({'code': 1000})  # 1000 every thing is ok
    else:
        return jsonify({'code': 1002})  # 1002 validcode send fail


# Check whether the input code is the same as the one sent to phone
@app.route('/code/<string:code>/validate/')
def code_validate(code):
    if code == session.get('valid_code'):
        return jsonify({'status': '100'})
    else:
        return jsonify({'status': '000'})

# Check whether the iphone has been registered already
@app.route('/phone/<string:phone>/check/')
def phone_check(phone):
    salesman = OzingSalesmanUser.query.filter_by(salesman_phone=phone).first()
    if salesman is None:
        return jsonify({'status': '100'})
    else:
        return jsonify({'status': '000'})


def insert_regions():
    db.drop_all(bind='regions')
    db.create_all(bind='regions')
    province_data, city_data, district_data = [], [], []
    payload = {'subdistrict': 3, 'key': AMAP_KEY}
    r = requests.get('https://restapi.amap.com/v3/config/district', params=payload)
    result = r.json()
    regions = result['districts'][0]['districts']
    for region in regions:
        province_data.append(region['name'])
        citys = region['districts']
        for city in citys:
            city_data.append((region['name'], city['name']))
            districts = city['districts']
            for district in districts:
                district_data.append((city['name'], district['name']))

    for province in province_data:
        p = Province(name=province)
        db.session.add(p)
    db.session.commit()

    pre_province = ''
    p_id = ''
    for city in city_data:
        p, c = city
        if p == pre_province:
            cit = City(name=c, province_id=p_id)
        else:
            pre_province = p
            prov = Province.query.filter_by(name=p).first()
            p_id = prov.id
            cit = City(name=c, province_id=p_id)
        db.session.add(cit)
    db.session.commit()

    pre_city = ''
    c_id = ''
    for district in district_data:
        c, d = district
        if c == pre_city:
            dist = District(name=d, city_id=c_id)
        else:
            pre_city = c
            cit = City.query.filter_by(name=c).first()
            c_id = cit.id
            dist = District(name=d, city_id=c_id)
        db.session.add(dist)
    db.session.commit()


# refresh region data
@app.route('/refresh_regions/', methods=['GET'])
def refresh_regions():
    insert_regions()
    return jsonify(True)


