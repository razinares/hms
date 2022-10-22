from application import *
from flask_migrate import Migrate
from datetime import *
import random

migrate = Migrate(app, db)








class Userstore(db.Model):
    __tablename__ = 'userstore'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20))
    password = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.now)

class Employee(db.Model):
    __tablename__ = 'employee_data'
    eid = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String(20), nullable=False)
    empid = db.Column(db.Integer, default=random.randint(10000, 99999))
    edesignation = db.Column(db.String(20))
    ecnum = db.Column(db.Integer)
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

class Patients(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    ssn_id = db.Column(db.Integer)
    pname = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)
    ldate = db.Column(db.DateTime, default=datetime.now)
    tbed = db.Column(db.String(10))
    address = db.Column(db.String(20))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    status = db.Column(db.String(20))

    # children = relationship("Medicines")
    # children1 = relationship("Diagnostics")

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
