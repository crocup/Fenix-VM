from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash,  check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class InventoryPost(db.Model):
    __tablename__ = 'inventory'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), default="None")
    dateofreg = db.Column(db.String(20))
    scanners = db.relationship('ScannerPost', backref='owner')

    def __init__(self, ip, dateofreg):
        self.ip = ip
        self.dateofreg = dateofreg


class ScannerPost(db.Model):
    __tablename__ = 'scanner'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    protocol = db.Column(db.String(10))
    port = db.Column(db.String(7))
    service_name = db.Column(db.String(20))
    service_version = db.Column(db.String(20))
    dateofreg = db.Column(db.String(20))
    owner_uid = db.Column(db.Integer, db.ForeignKey('inventory.uid'), nullable=False)


class ResultPost(db.Model):
    __tablename__ = 'result'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    dateofreg = db.Column(db.String(20))

    def __init__(self, uuid, name, dateofreg):
        self.uuid = uuid
        self.name = name
        self.dateofreg = dateofreg


db.create_all()
