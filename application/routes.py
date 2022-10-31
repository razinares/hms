from flask import *
import re
from application.db import *
import os, sys, subprocess
import uuid
import pdfkit
from application.rooms import *

# ROOM FUNCTIONS

# ARRAY OF ROOM AND BEDS


# END ROOM FUNCITONS

# Detects System for WKHTMLTOPDF
if sys.platform == "win32":
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
else:
        os.environ['PATH'] += os.pathsep + os.path.dirname(sys.executable)
        WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')],
            stdout=subprocess.PIPE).communicate()[0].strip()
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)



# path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


#SuperUser logging activity
def storeActivity(id, action):
    activity = UserActivity(userID=id, action=action)
    db.session.add(activity)
    db.session.commit()



# LOGIN START
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username') or session.get('recepUsername') or session.get('lab'):                # Checking for session login
        return redirect( url_for('home') )


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usr = Userstore.query.filter_by(uname = username).first()
        emp = Employee.query.filter_by(empid=username).first()
        if usr == None:
            if emp == None:
                flash('User Not Found', category='error')
                return redirect(url_for('login'))
            else:
                if emp.edesignation == "Receptionist":
                    if (username == str(emp.empid)) and (password == emp.emppassword):
                        session['recepUsername'] = username
                        return redirect(url_for('home'))
                elif emp.edesignation == "Lab":
                    if (username == str(emp.empid)) and (password == emp.emppassword):
                        session['lab'] = username
                        return redirect(url_for('home'))

                elif emp.edesignation == "Accounts":
                    if (username == str(emp.empid)) and (password == emp.emppassword):
                        session['accounts'] = username
                        return redirect(url_for('home'))

                elif emp.edesignation == "Pharmacy":
                    if (username == str(emp.empid)) and (password == emp.emppassword):
                        session['pharmacy'] = username
                        return redirect(url_for('home'))

                else:
                    return redirect(url_for(login))
        elif username == usr.uname and password == usr.password:
            storeActivity(usr.id, "Login")
            session['username'] = usr.id  # saving session for login

            return redirect( url_for('home') )

        else:
            flash('Wrong Credentials. Check Username and Password Again', category="error")

    return render_template("login.html")
# LOGIN END



# REGISTRATION START
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['pass']
        cnfrm_password = request.form['cpass']

        query = Userstore.query.filter_by(uname = uname).first()

        if query != None:
            if uname == str(query.uname):
                flash('Username already taken')
                return redirect( url_for('registration') )
        
        if password != cnfrm_password:
            flash('Passwords do not match')
            return redirect( url_for('registration') )

        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pattern = re.compile(regex)

        match = re.search(pattern, password)
        
        if match:
            user = Userstore(uname = uname, password = password)
            db.session.add(user)
            db.session.commit()
            flash('Staff Registred Successfully', category='info')
            return redirect( url_for('login') )
        else:
            flash('Password should contain one Uppercase, one special character, one numeric character')
            return redirect( url_for('registration') )
    return render_template('staff_registration.html')
# REGISTRATION END


# HOME
@app.route('/home')
def home():
    if (session.get('username') or session.get('recepUsername')) or (session.get('lab') or session.get('accounts')) or session.get('pharmacy'):
        return render_template('home.html')

    # elif 'recepUsername' in session:
    #     return render_template('home.html')
    # elif 'lab' in session:
    #     return render_template('home.html')
    else:
        flash('You are logged out. Please login again to continue')
        return redirect( url_for('login') )


# PATIENT START
# CREATE PATIENT
@app.route('/create_patient', methods=['GET', 'POST'])
def create_patient():
    if session.get('username') or session.get('recepUsername'):
        goom = avlRoom()
        gen = availRooms('General')
        semi = availRooms('Semi')
        single = availRooms('Single')
        if request.method == 'POST':
            assignBed = request.form['troom']
            nid = request.form['nid']
            pname = request.form['pname']
            age = request.form['age']
            tbed = request.form['tbed']
            address = request.form['address']
            pnum = request.form['pnum']
            anum = request.form['anum']
            status = request.form['status']
            issue = request.form['pproblem']
            pat = Patients.query.filter_by( nid = nid ).first()

            if pat == None:
                if availRooms(tbed) <= 0:
                    flash("No rooms left")
                    return redirect(url_for('create_patient'))
                patient = Patients(nid=nid, pname=pname, age=age, tbed=tbed, address=address, status = status, pcontact=pnum, assoc_contact=anum, issue=issue, room=tbed, assignBed=assignBed)
                bill = roomBill(tbed, 1)
                db.session.add(patient)
                try:
                    db.session.commit()
                    p = Patients.query.filter_by(nid=nid).first()
                    b = pbill(room=bill, pat=p.id)
                    db.session.add(b)
                    db.session.commit()
                except:
                    flash("Something went wrong")
                    return redirect(url_for('create_patient'))

                try:
                    storeActivity(session['username'], "Patient Created " + pname)
                except:
                    pass

                flash('Patient creation initiated successfully')
                return redirect( url_for('create_patient') )

            else:
                flash('Patient with this NID already exists')
                return redirect( url_for('create_patient') )
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"
    return render_template('create_patient.html', gen=gen,semi=semi,single=single, avl=goom)

#UPDATE PATIENT
@app.route('/update_patient')
def update_patient():
    if session.get('username') or session.get('recepUsername'):
        updatep = Patients.query.all()
        if not updatep:
            flash('No patients exists in database')
            return redirect( url_for('create_patient') )
        else:
            print("inside else")
            return render_template('update_patient.html', updatep = updatep)
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


# DELETE PATIENT
@app.route('/deletepat')
def deletepat():
    if session.get('username') or session.get('recepUsername'):
        updatep = Patients.query.all()
        if not updatep:
            flash('No patients exists in database')
            return redirect( url_for('create_patient') )
        else:
            print("inside else")
            return render_template('deletepat.html', updatep = updatep)
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"

# EDIT PATIENT DETAILS
@app.route('/editpatientdetail/<id>', methods=['GET', 'POST'])
def editpatientdetail(id):
    print("id is : ", id)
    if session.get('username') or session.get('recepUsername'):
        print(datetime.now())
        editpat = Patients.query.filter_by( id = id )
        if request.method == 'POST':
            print("inside editpat post mtd")
            pname = request.form['npname']
            age = request.form['nage']
            tbed = request.form['tbed']
            address = request.form['naddress']
            status = request.form['status']
            ldate = datetime.today()
            row_update = Patients.query.filter_by( id = id ).update(dict(pname=pname, age=age, tbed=tbed, address=address, status = status, ldate=ldate))
            db.session.commit()
            try:
                storeActivity(session['username'], "Updated Details for Patient ID: " + id)
            except:
                pass
            print("Roww update", row_update)

            if row_update == None:
                flash('Something Went Wrong')
                return redirect( url_for('update_patient') )
            else:
                flash('Patient update initiated successfully')
                return redirect( url_for('update_patient') )

        return render_template('editpatientdetail.html', editpat = editpat)
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"

#DELETE PATIENT DETAILS
@app.route('/deletepatientdetail/<id>')
def deletepatientdetail(id):
    if session.get('username') or session.get('recepUsername'):
        delpat = Patients.query.filter_by(id = id).delete()
        med = Medicines.query.filter_by(pid=id).delete()
        dia = Diagnostics.query.filter_by(pid=id).delete()
        doc = DoctorVisit.query.filter_by(pid=id).delete()
        bill = pbill.query.filter_by(pat=id).delete()
        try:
            storeActivity(session['username'], "Patient Deleted ID " + id)
        except:
            pass
        db.session.commit()

        if (delpat or med or dia or doc or bill) == None:
            flash('Something Went Wrong')
            return redirect( url_for('update_patient') )
        else:
            flash('Patient deletion initiated successfully')
            return redirect( url_for('deletepat') )

    return render_template('update_patient.html')

# ACTIVE PATIENTS
@app.route('/patientscreen')
def patientscreen():
    if session.get('username') or session.get('recepUsername'):
        pts = Patients.query.filter_by( status = 'Active' )
        print("ptsss",pts)
        if not pts:
            flash('All Patients Discharged')
            return redirect( url_for('update_patient') )
        else:
            print("inside else")
            return render_template('patientscreen.html', pts = pts)

    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


# SEARCH PATIENT
@app.route('/search_patient', methods=['GET', 'POST'])
def search_patient():
    if session.get('username') or session.get('recepUsername'):
        allp = Patients.query.all()
        if request.method == 'POST':
            id = request.form['id']
            if id != "":
                patient = Patients.query.filter_by( id = id).first()
                if patient == None:
                    flash('No Patients with  this ID exists')
                    return redirect( url_for('search_patient') )
                else:
                    flash('Patient Found')
                    return render_template('search_patient.html', patient = patient, allp=allp)
            if id == "":
                flash('Enter  id to search')
                return redirect( url_for('search_patient') )

    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


    return render_template('search_patient.html', allp=allp)
# PATIENT END

# BILLING START
@app.route('/billing', methods=['GET', 'POST'])
def billing():
    global mtot, tot
    today = datetime.now()
    if (session.get('username') or session.get('recepUsername')) or session.get('accounts'):
        if request.method == 'POST':
            id = request.form['id']
            delta = 0
            if id != "":
                patient = Patients.query.filter_by( id = id).first()
                if patient == None:
                    flash('No Patients with that this ID exists')
                    return redirect( url_for('billing') )
                elif patient.status != 'Active':
                    flash('No Active Patients with Entered ID')

                else:
                    b = pbill.query.filter_by(pat=id).first()
                    flash('Patient Found')
                    x = patient.date
                    y = x.strftime("%d-%m-%Y, %H:%M:%S")
                    delta = ( today - x ).days
                    print(delta)
                    dy = 0
                    if delta == 0:
                        dy = 1
                    else:
                        dy = delta
                    roomtype = patient.tbed
                    bill = roomBill(roomtype, dy)
                    try:
                        update = pbill.query.filter_by(pat=id).update(dict(room=bill))
                        db.session.commit()
                    except:
                        flash("Something went wrong while generating bill")
                        return redirect(url_for('bg'))

                    med = Medicines.query.filter_by(pid = id).all()
                    if med == None:
                        flash('But No Medicines issued to Patient till Now')
                    else:
                        mtot = 0
                        for j in med:
                            mtot += (j.qissued * j.rate)

                    dia = Diagnostics.query.filter_by(pid = id).all()
                    if dia == None:
                        flash('But No Tests issued to Patient till Now')
                    else:
                        tot = 0
                        for i in dia:
                            tot += i.tcharge

                    doc = DoctorVisit.query.filter_by(pid=id).all()
                    if doc == None:
                        flash("No doctors made visit")
                    else:
                        d = 0
                        for j in doc:
                            d += j.charge
                        return render_template('newbill.html', patient = patient, dy=dy, y=y, bill = bill, med = med, dia = dia, mtot = mtot, tot = tot, i = d, doc=doc, b=b)
            if id == "":
                flash('Enter  id to search patient')
                return redirect( url_for('billing') )
    else:
        return redirect( url_for('login') )

    return render_template('newbill.html', allp=Patients.query.all())

# BILL GENERATE FOR PDF
@app.route('/generatebill/<id>')
def generatebill(id):
    global d
    dy = 0
    today = datetime.now()
    med = Medicines.query.filter_by(pid=id).all()
    patient = Patients.query.filter_by(id=id).first()
    dia = Diagnostics.query.filter_by(pid=id).all()
    doc = DoctorVisit.query.filter_by(pid=id).all()
    b = pbill.query.filter_by(pat=id).first()
    y = 0
    bill = 0
    mtot = 0
    tot = 0
    if id != "":

        if patient == None:
            flash('No Patients with that this ID exists')
            return redirect(url_for('billing'))
        elif patient.status != 'Active':
            flash('No Active Patients with Entered ID')

        else:
            x = patient.date
            y = x.strftime("%d-%m-%Y, %H:%M:%S")
            delta = (today - x).days
            print(delta)
            if delta == 0:
                dy = 1
            else:
                dy = delta
            roomtype = patient.tbed
            print(roomtype)
            if roomtype == 'Single':
                bill = 8000 * dy
            elif roomtype == 'Semi':
                bill = 4000 * dy
            else:
                bill = 2000 * dy

            if med == None:
                flash('But No Medicines issued to Patient till Now')
            else:
                mtot = 0
                for j in med:
                    mtot += (j.qissued * j.rate)

            if dia == None:
                flash('But No Tests issued to Patient till Now')
            else:
                tot = 0
                for i in dia:
                    tot += i.tcharge

            if doc == None:
                flash('No doctors made visit')
            else:
                d = 0
                for j in doc:
                    d += j.charge

    if id == "":
        return redirect(url_for('billing'))

    if session.get('username') or session.get('accounts'):
        stat = 'Discharged'
        row_update = Patients.query.filter_by( id = id ).update(dict(status = stat))
        db.session.commit()
        try:
            storeActivity(session['username'], "Bill Generated for Patient ID: " + id)
        except:
            pass
        if row_update == None:
            flash('Something Went Wrong')
            return redirect( url_for('billing') )
        else:
            html = render_template(
                "printbill.html",
                patient=patient, dy=dy, y=y, bill=bill, med=med, dia=dia, mtot=mtot, tot=tot, i=d, doc=doc, b=b
            )
            css = ['application/static/css/main.css']
            pdf = pdfkit.from_string(html, False, configuration=pdfkit_config, css=css)
            response = make_response(pdf)
            response.headers["Content-Type"] = "application/pdf"
            response.headers['Content-Disposition'] = \
                'inline; filename=%s.pdf' % 'output'
            return response
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


# DOCTOR VISIT
@app.route('/doctor_visit', methods=['GET', 'POST'])
def doctor_visit():
    if (session.get('username') or session.get('accounts')):
        if request.method == 'POST':
            dname = request.form['dname']
            pid = request.form['pid']
            fee = request.form['fee']
            dc = Patients.query.filter_by(id=pid).first()
            bill = pbill.query.filter_by(id=pid).first()
            if bill == None:
                v = pbill(doc=fee, pat=pid)
                db.session.add(v)

            else:
                newBill = bill.doc + int(fee)
                new = str(newBill)
                row_update = pbill.query.filter_by(pat=pid).update(dict(doc=new))
            if dc == None:
                flash("No patients found with this patient ID")
                return redirect(url_for('doctor_visit'))
            doc = DoctorVisit(dname=dname, pid=pid, charge=fee)
            try:
                db.session.add(doc)
                db.session.commit()
                flash("Successfully added")
                return redirect(url_for('doctor_visit'))

            except:
                flash("Something went wrong")
                return redirect(url_for('doctor_visit'))

    return render_template('docVisit.html')


# DISCOUNT
@app.route('/discount/<id>', methods=['GET', 'POST'])
def discount(id):
    if session.get('username') or session.get('accounts'):
        if request.method == "POST":
            discount = request.form['discount']
            p = pbill.query.filter_by(pat=id).first()
            bill = (p.doc + p.room + p.med + p.diag) - (p.discount + p.paid)
            if int(discount) < 1:
                flash("Discount cannot be less than 1")
                return redirect(url_for("bg"))
            elif float(discount) > ((bill * 50) / 100):
                flash("Discount cannot be greater than 50%")
                return redirect(url_for('billing'))
            else:
                row_update = pbill.query.filter_by(pat=id).update(dict(discount=discount))
                try:
                    db.session.commit()
                    flash("Discount has been added successfully")
                    return redirect(url_for('billing'))
                except:
                    flash("Couldn't add discount.")
                    return redirect(url_for('billing'))
    else:
        return redirect(url_for('login'))


# PAY BILL ADVANCE
@app.route('/paybill/<id>', methods=['GET', 'POST'])
def paybill(id):
    if session.get('username') or session.get('accounts'):
        if request.method == "POST":
            amount = request.form['amount']
            p = pbill.query.filter_by(pat=id).first()
            bill = (p.doc + p.room + p.med + p.diag) - (p.discount + p.paid)
            if int(amount) > bill:
                flash("Bill pay amount cannot be greater than the bill itself")
                return redirect(url_for('billing'))
            row = pbill.query.filter_by(pat=id).update(dict(paid=amount))
            try:
                db.session.commit()
                flash("Bill paid successfully")
                return redirect(url_for('billing'))
            except:
                flash("Couldn't pay bill")
                return redirect(url_for('billing'))

    else:
        return redirect(url_for('login'))


# BILLING END


# MEDICINE START
# ADD MEDICINE
@app.route('/addMedicine', methods=['GET', 'POST'] )
def addMedicine():
    if (session.get('username') or session.get('lab')) or session.get('pharmacy'):
        if request.method == 'POST':
            mid = request.form['mid']
            mname = request.form['mname']
            qavailable = request.form['qavailable']
            rate = request.form['rate']

            pat = MedicineMaster.query.filter_by( mid = mid ).first()

            if pat == None:
                med = MedicineMaster(mid=mid, mname=mname, qavailable=qavailable, rate=rate)
                db.session.add(med)
                db.session.commit()
                try:
                    storeActivity(session['username'], "Added Medicine " + mname)
                except:
                    pass
                flash('Medicine successfully Inserted to Database')
                return redirect( url_for('addMedicine') )

            else:
                flash('Medicine with this  ID already exists')
                return redirect( url_for('addMedicine') )
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"

    return render_template('addMedicine.html')



# ISSUE MEDICINE
@app.route('/PharmacistPatientDetails', methods=['GET', 'POST'])
def PharmacistPatientDetails():
    if session.get('username') or session.get('pharmacy'):
        if request.method == 'POST':
            id = request.form['id']

            if id != "":
                patient = Patients.query.filter_by( id = id).first()
                if patient == None:
                    flash('No Patients with that this ID exists')
                    return redirect( url_for('PharmacistPatientDetails') )
                else:
                    flash('Patient Found')

                med = Medicines.query.filter_by(pid = id).all()
                print("Meddd", med)
                if med == None:
                    flash('No Medicines issued to Patient till Now')
                    return render_template('PharmacistPatientDetails.html', patient = patient)
                else:
                    return render_template('PharmacistPatientDetails.html',patient = patient, med = med)

            if id == "":
                flash('Enter  id to search')
                return redirect( url_for('PharmacistPatientDetails') )

    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"

    return render_template('PharmacistPatientDetails.html', allp=Patients.query.all())


# MEDICINE LISTS
@app.route('/medicinestatus')
def medicinestatus():
    if (session.get('username') or session.get('pharmacy')):
        updatep = MedicineMaster.query.all()
        print(updatep)
        if not updatep:
            flash('No Medicines exists in database')
            return redirect( url_for('addMedicine') )
        else:
            print("inside else")
            return render_template('medicinestatus.html', updatep = updatep)

    else:
        # flash('You have been logged out. Please login again')
        # return redirect( url_for('login') )
        return "<h1>You do not have permission to perform this action. Please go back</h1>"
    # return render_template('medicinestatus.html')


# UPDATE MEDICINE
@app.route('/updatemed')
def updatemed():
    if (session.get('username') or session.get('pharmacy')):

        updatep = MedicineMaster.query.all()
        print(updatep)
        if not updatep:
            flash('No Medicines exists in database')
            return redirect( url_for('addMedicine') )
        else:
            print("inside else")
            return render_template('updatemed.html', updatep = updatep)

    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


# DELETE MEDICINE
@app.route('/deletemed')
def deletemed():
    if (session.get('username') or session.get('pharmacy')):
        updatep = MedicineMaster.query.all()
        print(updatep)
        if not updatep:
            flash('No Medicines exists in database')
            return redirect( url_for('addMedicine') )
        else:
            print("inside else")
            return render_template('deletemed.html', updatep = updatep)
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


# EDIT MEDICINE DETAILS
@app.route('/editmedicinedetail/<mid>', methods=['GET', 'POST'] )
def editmedicinedetail(mid):
    print("id is : ", mid)
    if (session.get('username') or session.get('pharmacy')):
        print("inside sesssss")
        print(datetime.now())
        editpat = MedicineMaster.query.filter_by( mid = mid )

        if request.method == 'POST':
            print("inside editpat post mtd")
            mname = request.form['mname']
            qavailable = request.form['qavailable']
            rate = request.form['rate']
            row_update = MedicineMaster.query.filter_by( mid = mid ).update(dict(mname=mname, qavailable=qavailable, rate=rate))
            db.session.commit()
            try:
                storeActivity(session['username'], "Medicine Details Modified: " + mname)
            except:
                pass
            print("Roww update", row_update)

            if row_update == None:
                flash('Something Went Wrong')
                return redirect( url_for('medicinestatus') )
            else:
                flash('Patient update initiated successfully')
                return redirect( url_for('medicinestatus') )

        return render_template('editmedicinedetail.html', editpat = editpat)


# DELETE MEDICINE
@app.route('/deletemedicinedetail/<mid>')
def deletemedicinedetail(mid):
    if (session.get('username') or session.get('pharmacy')):
        delpat = MedicineMaster.query.filter_by(mid = mid).delete()
        db.session.commit()
        try:
            storeActivity(session['username'], "Medicine Removed ID:" + mid)
        except:
            pass

        if delpat == None:
            flash('Something Went Wrong')
            return redirect( url_for('medicinestatus') )
        else:
            flash('Medicine deletion initiated successfully')
            return redirect( url_for('deletemed') )

    return render_template('medicinestatus.html')


# ISSUE MEDICINE
@app.route('/issuemedicine/<pid>', methods=['GET', 'POST'])
def issuemedicine(pid):
    if session.get('username') or session.get('pharmacy'):
        allm = allm=MedicineMaster.query.all()
        if request.method == 'POST':
            mname = request.form['mname']

            if mname != "":
                patient = MedicineMaster.query.filter_by( mname = mname).first()
                if patient == None:
                    flash('No Medicine with this Name exists')
                    return render_template('issuemedicine.html', allm=allm)
                else:
                    flash('Medicine found')
                    qissued = request.form['qissued']
                    qid = int(qissued)
                    print( type(qid) )
                    print((patient.qavailable) - qid)
                    if(qid > patient.qavailable):
                        flash("Entered Medicine Quantity Unavailable")
                        return render_template('issuemedicine.html', patient = patient, allm=allm)
                    else:
                        patient.qavailable = patient.qavailable - qid
                        db.session.commit()
                        mid = patient.mid
                        rate = patient.rate
                        bill = pbill.query.filter_by(id=pid).first()
                        tot = rate*qid
                        if bill == None:
                            v = pbill(med=tot, pat=pid)
                            db.session.add(v)

                        else:
                            newBill = bill.med + int(tot)
                            new = str(newBill)
                            row_update = pbill.query.filter_by(pat=pid).update(dict(med=new))
                        rowup = Medicines( mid = mid, pid=pid, mname = mname, rate = rate , qissued=qissued)
                        db.session.add(rowup)
                        db.session.commit()
                        try:
                            storeActivity(session['username'], "Medicine Issued to Patient ID: " + pid)
                        except:
                            pass
                        return render_template('issuemedicine.html', patient = patient, allm=allm)

            if mname == "":
                flash('Enter  Medicine Name to Search')
                return render_template('issuemedicine.html', allm=allm)

    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"

    return render_template('issuemedicine.html', allm=MedicineMaster.query.all())
# MEDICINE END


# DIAGNOSTICS START
# ISSUE DIAGNOSTICS
@app.route('/DiagnosticsPatientDetails', methods=['GET', 'POST'])
def DiagnosticsPatientDetails():
    if session.get('username') or session.get('lab'):
        if request.method == 'POST':
            id = request.form['id']

            if id != "":
                patient = Patients.query.filter_by( id = id).first()
                if patient == None:
                    flash('No Patients with that this ID exists')
                    return redirect( url_for('DiagnosticsPatientDetails') )
                else:
                    flash('Patient Found')

                med = Medicines.query.filter_by(pid = id).all()
                print("Meddd", med)
                if med == None:
                    flash('But No Medicines issued to Patient till Now')
                    return render_template('DiagnosticsPatientDetails.html', patient = patient)
                dia = Diagnostics.query.filter_by(pid = id).all()
                if dia == None:
                    flash('But No Tests issued to Patient till Now')
                    return render_template('DiagnosticsPatientDetails.html', patient = patient)
                else:
                    return render_template('DiagnosticsPatientDetails.html',patient = patient, med = med, dia = dia)

            if id == "":
                flash('Enter  id to search')
                return redirect( url_for('DiagnosticsPatientDetails') )

    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"

    return render_template('DiagnosticsPatientDetails.html', allp=Patients.query.all())


# ADD DIAGNOSTICS
@app.route('/addDiagnostics', methods=['GET', 'POST'] )
def addDiagnostics():
    if session.get('username') or session.get('lab'):
        if request.method == 'POST':
            tid = request.form['tid']
            tname = request.form['tname']
            tcharge = request.form['tcharge']

            pat = DiagnosticsMaster.query.filter_by( tid = tid ).first()

            if pat == None:
                diag = DiagnosticsMaster(tid=tid, tname=tname, tcharge=tcharge)
                db.session.add(diag)
                db.session.commit()
                try:
                    storeActivity(session['username'], "Added Diagnostics " + tname)
                except:
                    pass
                flash('Test successfully Added to Database')
                return redirect( url_for('addDiagnostics') )

            else:
                flash('Test with this  ID already exists')
                return redirect( url_for('addDiagnostics') )
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"

    return render_template('addDiagnostics.html')


# DIAGNOSTICS LIST
@app.route('/diagnosticsstatus')
def diagnosticsstatus():
    if session.get('username') or session.get('lab'):
        updatep = DiagnosticsMaster.query.all()
        print(updatep)
        if not updatep:
            flash('No Tests Available')
            return redirect( url_for('addDiagnostics') )
        else:
            print("inside else")
            return render_template('diagnosticsstatus.html', updatep = updatep)
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


# ISSUE DIAGNOSTICS
@app.route('/issuediagnostics/<pid>', methods=['GET', 'POST'])
def issuediagnostics(pid):
    if session.get('username') or session.get('lab'):
        alld = DiagnosticsMaster.query.all()
        if request.method == 'POST':
            tname = request.form['tname']
            
            if tname != "":
                patient = DiagnosticsMaster.query.filter_by( tname = tname).first()
                if patient == None:
                    flash('No Test with this Name exists')
                    return render_template('issuediagnostics.html', alld=alld)
                else:
                    flash('Test Found')
                    tid = patient.tid
                    tcharge = patient.tcharge
                    bill = pbill.query.filter_by(id=pid).first()
                    if bill == None:
                        v = pbill(diag=tcharge, pat=pid)
                        db.session.add(v)

                    else:
                        newBill = bill.diag + int(tcharge)
                        new = str(newBill)
                        row_update = pbill.query.filter_by(pat=pid).update(dict(diag=new))
                    rowup = Diagnostics( tid = tid, pid=pid, tname = tname, tcharge = tcharge )
                    db.session.add(rowup)
                    db.session.commit()
                    try:
                        storeActivity(session['username'], "Issued Diagnostic to Patient ID: " + pid)
                    except:
                        pass
                    return render_template('issuediagnostics.html', patient = patient, alld=alld)
      
            if tname == "":
                flash('Enter  Test Name to Search')
                return redirect(url_for('issuediagnostics'))
    
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"
    
    return render_template('issuediagnostics.html', alld=alld)


# DELETE DIAGNOSTICS
@app.route('/delete_diagnostics')
def delete_diagnostics():
    if (session.get('username') or session.get('lab')):
        updatep = DiagnosticsMaster.query.all()
        print(updatep)
        if not updatep:
            flash('No Diagnostics exists in database')
            return redirect( url_for('addDiagnostics') )
        else:
            print("inside else")
            return render_template('deleteDiagnostics.html', updatep = updatep)

    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


# DELETE DIAGNOSTICS
@app.route('/deletediadetail/<mid>')
def deletediadetail(mid):
    if (session.get('username') or session.get('lab')):
        delpat = DiagnosticsMaster.query.filter_by(tid = mid).delete()
        db.session.commit()
        try:
            storeActivity(session['username'], "Medicine Removed ID:" + mid)
        except:
            pass

        if delpat == None:
            flash('Something Went Wrong')
            return redirect( url_for('medicinestatus') )
        else:
            flash('Diagnostics deletion initiated successfully')
            return redirect( url_for('delete_diagnostics') )


# UPDATE DIAGNOSTICS
@app.route('/updateDiagnostics')
def updatediag():
    if (session.get('username') or session.get('lab')):

        updatep = DiagnosticsMaster.query.all()
        print(updatep)
        if not updatep:
            flash('No Medicines exists in database')
            return redirect( url_for('addDiagnostics') )
        else:
            print("inside else")
            return render_template('updateDiagnostics.html', updatep = updatep)

    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


# UPDATE DIAGNOSTICS DETAILS
@app.route('/updatediadetails/<mid>', methods=['GET', 'POST'] )
def updatediadetails(mid):
    if (session.get('username') or session.get('lab')):
        editpat = DiagnosticsMaster.query.filter_by( tid = mid )
        if request.method == 'POST':
            mname = request.form['mname']
            rate = request.form['rate']
            row_update = DiagnosticsMaster.query.filter_by( tid = mid ).update(dict(tname=mname, tcharge=rate))
            db.session.commit()
            try:
                storeActivity(session['username'], "Diagnostics Details Modified: " + mname)
            except:
                pass
            if row_update == None:
                flash('Something Went Wrong')
                return redirect( url_for('diagnosticsstatus') )
            else:
                flash('Diagnostics update initiated successfully')
                return redirect( url_for('diagnosticsstatus') )

        return render_template('editdiadetails.html', editpat=editpat)


# EMPLOYEE START
# ADD EMPLOYEE
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'username' in session:
       if request.method == 'POST':
           ename = request.form['ename']
           empid = request.form['empid']

           edesignation = request.form['edesignation']
           ecnum =request.form['ecnum']
           efname = request.form['efname']
           emname = request.form['emname']
           eenum = request.form['eenum']
           enid = request.form['enid']
           paddr = request.form['paddr']
           edob = request.form['edob']
           epaddress = request.form['epaddress']
           emppassword = request.form['password']
           ephoto = request.files['ephoto']
           eedu = request.form['eedu']
           ejobinfo = request.form['ejobinfo']
           if empid == None:
               empid = random.randint(10000, 99999)
           uid = str(uuid.uuid4())
           ephotoname = uid + str(ephoto.filename)
           ephoto.save(os.path.join('application/static/ephotos', ephotoname))
           if not ephoto:
               ephotoname = None
           employee = Employee(ename=ename, edesignation=edesignation, ephoto=ephotoname, emppassword=emppassword, empid=empid, ecnum=ecnum, efname=efname, emname=emname, eenum=eenum, paddr=paddr, edob=edob, epaddress=epaddress, enid=enid, eedu=eedu, ejobinfo=ejobinfo)
           db.session.add(employee)
           db.session.commit()
           try:
               storeActivity(session['username'], "Added Employee " + ename)
           except:
               pass
           flash('Employee successfully added')
           return redirect(url_for('add_employee'))


       employees = Employee.query.all()
       return render_template('CreateEmployee.html', employees=employees)


    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"

# LIST EMPLOYEE
@app.route('/list_employees', methods=['GET'])
def list_employees():
    if 'username' in session:
        employees = Employee.query.all()
        return render_template('listEmployees.html', employees=employees)
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


# REMOVE EMPLOYEE
@app.route('/remove_employee')
def remove_employees():
    if 'username' in session:
        employees = Employee.query.all()
        return render_template('removeEmployee.html', employees=employees)
    else:
        return redirect(url_for('home'))

# REMOVE EMPLOYEE
@app.route('/remove_employee/<id>')
def remove_employee(id):
    if 'username' in session:
        emp = Employee.query.filter_by(eid = id).delete()
        db.session.commit()
        storeActivity(session['username'], "Removed Employee ID: " + id)

        if emp == None:
            flash('Something Went Wrong')
            return redirect( url_for('list_employees') )
        else:
            flash('Employee deletion initiated successfully')
            return redirect( url_for('remove_employees') )

    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"


# EDIT EMPLOYEE
@app.route('/edit_employee/<id>', methods=['GET', 'POST'])
def edit_employee(id):
    print("id is : ", id)
    if session.get('username'):
        print(datetime.now())
        emp = Employee.query.filter_by( eid = id )


        if request.method == 'POST':
            pname = request.form['npname']
            address = request.form['naddress']
            edesignation = request.form['edesignation']
            ecnum = request.form['ncontact']
            password = request.form['password']
            row_update = Employee.query.filter_by( eid = id ).update(dict(ename=pname, epaddress=address, edesignation=edesignation, ecnum=ecnum, emppassword=password))
            db.session.commit()
            try:
                storeActivity(session['username'], "Updated Details for Patient ID: " + id)
            except:
                pass

            if row_update == None:
                flash('Something Went Wrong')
                return redirect( url_for('update_patient') )
            else:
                flash('Employee update initiated successfully')
                return redirect( url_for('update_patient') )

        return render_template('editEmployee.html', editpat = emp)
    else:
        return "<h1>You do not have permission to perform this action. Please go back</h1>"

# VIEW EMPLOYEE
@app.route('/view_employee/<id>')
def view_employee(id):
    if 'username' in session:
        employee = Employee.query.filter_by(eid = id).first()
        return render_template('viewEmployee.html', employee=employee)

    else:
        return redirect(url_for('home'))
#  END EMPLOYEE

# SUPERUSER LOGS
@app.route('/user_activity')
def user_activity():
    if 'username' in session:
        activities = UserActivity.query.order_by(UserActivity.id.desc()).limit(50).all()
        return render_template('userActivity.html', activities = activities)

    else:
        return redirect(url_for('login'))


# LOGOUT FOR ALL USER
@app.route('/logout')
def logout():
    session.clear()
    flash('logged out successfully .')
    return redirect( url_for('login') )




