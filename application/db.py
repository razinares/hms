from application import *
from flask_migrate import Migrate
from datetime import *
import random

migrate = Migrate(app, db)


class Userstore(db.Model):
    __tablename__ = 'userstore'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    activity = db.relationship('UserActivity', backref='user')



class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('userstore.id'))
    action = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now())


class Employee(db.Model):
    __tablename__ = 'employee_data'
    eid = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String(20), nullable=False)
    empid = db.Column(db.Integer, default=random.randint(10000, 99999), unique=True)
    edesignation = db.Column(db.String(20))
    ecnum = db.Column(db.String(20))
    efname = db.Column(db.String(20))
    emname = db.Column(db.String(20))
    eenum = db.Column(db.String(20))
    enid = db.Column(db.Integer)
    paddr = db.Column(db.String)
    edob = db.Column(db.String(20))
    epaddress = db.Column(db.String)
    eedu = db.Column(db.String)
    ejobinfo = db.Column(db.String)
    ephoto = db.Column(db.String(255), nullable=False, default="default.jpg")
    emppassword = db.Column(db.String(255), nullable=False, default="hospital")

class Patients(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    nid = db.Column(db.Integer, unique=True)
    pname = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)
    ldate = db.Column(db.DateTime, default=datetime.now)
    tbed = db.Column(db.String(10))
    address = db.Column(db.String(20))
    # city = db.Column(db.String(20))
    # state = db.Column(db.String(20))
    status = db.Column(db.String(20))
    issue = db.Column(db.String(100))
    pcontact = db.Column(db.String(20))
    assoc_contact = db.Column(db.String(20))
    room = db.Column(db.String(9))


class Medicines(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    mname = db.Column(db.String(20))
    mid = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    qissued = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)

    children = db.relationship("MedicineMaster")

class MedicineMaster(db.Model):
    __tablename__ = 'medicinemaster'
    mid = db.Column(db.Integer, db.ForeignKey('medicines.mid'), primary_key=True)
    mname = db.Column(db.String(20))
    qavailable = db.Column(db.Integer)
    rate = db.Column(db.Integer)

class Diagnostics(db.Model):
    __tablename__ = 'diagnostics'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    tname = db.Column(db.String(20))
    tid = db.Column(db.Integer)
    tcharge = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)

    children = db.relationship("DiagnosticsMaster")

class DiagnosticsMaster(db.Model):
    __tablename__ = 'diagnosticsmaster'
    tid = db.Column(db.Integer, db.ForeignKey('diagnostics.tid'), primary_key=True)
    tname = db.Column(db.String(20))
    tcharge = db.Column(db.Integer)

class DoctorVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    dname = db.Column(db.String(20))
    charge = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now())


class pbill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.Integer, nullable=False, default=0)
    diag = db.Column(db.Integer, nullable=False, default=0)
    doc = db.Column(db.Integer, nullable=False, default=0)
    med = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.DateTime, default=datetime.now())
    pat = db.Column(db.Integer, nullable=False, unique=True)
    paid = db.Column(db.Integer, nullable=False, default=0)
    discount = db.Column(db.Integer, nullable=False, default=0)





