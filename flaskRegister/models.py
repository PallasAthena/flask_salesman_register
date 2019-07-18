from flaskRegister import db


class OzingSalesmanUser(db.Model):
    __tablename__ = 'ozing_salesman_user'
    salesman_id = db.Column(db.Integer, primary_key=True)
    salesman_name = db.Column(db.VARCHAR(255))
    salesman_phone = db.Column(db.VARCHAR(20))
    province = db.Column(db.VARCHAR(20))
    city = db.Column(db.VARCHAR(20))
    district = db.Column(db.VARCHAR(20))
    endpoint = db.Column(db.VARCHAR(255))
    sex = db.Column(db.VARCHAR(2))
    wx_id = db.Column(db.VARCHAR(255))
    sold_products = db.relationship('ValidSoldProduct', backref='salesman', lazy='dynamic')

    def __repr__(self):
        return f'<OzingSalesmanUser: {self.salesman_name} - {self.salesman_phone}>'


class Province(db.Model):
    __bind_key__ = 'regions'
    __tablename__ = 'provinces'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100))
    cities = db.relationship('City', backref='province', lazy='dynamic')

    def __repr__(self):
        return f'<Province: {self.name}>'


class City(db.Model):
    __bind_key__ = 'regions'
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100))
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'))
    districts = db.relationship('District', backref='city', lazy='dynamic')

    def __repr__(self):
        return f'<Province: {self.name}>'


class District(db.Model):
    __bind_key__ = 'regions'
    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))

    def __repr__(self):
        return f'<Province: {self.name}>'


class SalesmanSoldProduct(db.Model):
    __tablename__ = 'ozing_salesman_cust_mac'
    salesman_cust_mac_id = db.Column(db.Integer, primary_key=True)
    is_valid = db.Column(db.VARCHAR(2))

    __mapper_args__ = {
        'polymorphic_on': is_valid
    }



class ValidSoldProduct(SalesmanSoldProduct):
    device_number = db.Column(db.VARCHAR(255))
    create_time = db.Column(db.DateTime)
    salesman_id = db.Column(db.Integer, db.ForeignKey('ozing_salesman_user.salesman_id'))

    __mapper_args__ = {
        'polymorphic_identity': '1'
    }

