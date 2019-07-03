from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, InputRequired
from flask import session
from flaskRegister.models import OzingSalesmanUser, Province, City, District


class SalesmanForm(FlaskForm):
    province = SelectField('省', coerce=int, validators=[DataRequired('请选择省')])
    city = SelectField('市', coerce=int, validators=[DataRequired('请选择市')])
    district = SelectField('区/县',  coerce=int, validators=[DataRequired('请选择区/县')])
    endpoint = StringField('终端名称', validators=[InputRequired('请输入终端姓名')])
    name = StringField('姓名', validators=[InputRequired('请输入姓名')])
    phonenumber = StringField('手机号码', validators=[InputRequired('请输入电话号码')])
    validcode = StringField('验证码', validators=[InputRequired('请输入验证码')])
    gender = SelectField('性别', coerce=int, validators=[DataRequired('请选择性别')])
    weichat_id = StringField('微信号')
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(SalesmanForm, self).__init__(*args, **kwargs)
        province_choices = [(0, '请选择省')]
        province_choices.extend([(province.id, province.name) for province in Province.query.all()])
        self.province.choices = province_choices

        city_choices = [(0, '请选择市')]
        city_choices.extend([(city.id, city.name) for city in City.query.all()])
        self.city.choices = city_choices

        district_choices = [(0, '请选择区/县')]
        district_choices.extend([(district.id, district.name) for district in District.query.all()])
        self.district.choices = district_choices

        self.gender.choices=[(0, '请选择性别'),(1, '女'), (2, '男')]

    def validate_phonenumber(self, phonenumber):
        salesman = OzingSalesmanUser.query.filter_by(salesman_phone=phonenumber.data).first()
        if salesman is not None:
            raise ValidationError('此手机号已经注册')

    def validate_validcode(self, validcode):
        print(f'session_phone={session.get("phone")}')
        print(f'phonenumber={self.phonenumber.data}')
        if session.get('valid_code') != validcode.data or session.get('phone') != self.phonenumber.data:
            raise ValidationError('验证码错误，请检查验证码')




