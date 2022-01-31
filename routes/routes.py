import jwt
from datetime import datetime, timedelta
from functools import wraps
from forms import LoginForm, Admin_Login, RegistrationForm
from flask import render_template, url_for, flash, redirect, make_response, session, request, jsonify
from models.model import *
from app import app

def token_required(f):
   @wraps(f)
   def decorated(*args, **kwargs):
      token = None
      # jwt is passed in the request header
      if 'x-access-token' in request.headers:
         token = request.headers['x-access-token']
      # return 401 if token is not passed
      if not token:
         return jsonify({'message' : 'Token is missing'}), 401
      try:
         data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
         email = data['email']
         password = data['password']
         current_user = User.query.filter_by(email=email)
      except:
         return jsonify({'message' : 'Token is invalid'}), 401
      # returns the current logged in users contex to the routes
      return f(current_user, *args, **kwargs)
   return decorated
def OAuth(Token):
    try:
        data = jwt.decode(Token, app.config['SECRET_KEY'], algorithms=["HS256"])
        email = data['email']
        password = data['password']
        N = User.query.filter_by(email=email)
        if N[0].email == email and N[0].password == password:
          session['Token'] = Token
          session['username'] = data['username']
          M = [S for S in History.query.all() if S.Access_Token == session.get('Token')]
          HS = History.query.all()
          session['Task_Done'] = "Successfully Logged in"
          return make_response(render_template('index.html', Page="", Authenticated=True, id=N[0].id, username=N[0].username ,M=M ,access_token=N[0].Access_Token, password=N[0].password, Title=session.get('username'),History=HS))
    except:
            return make_response(redirect('/index'))
def Main():
    try:
        if session.get('Token') != None:
           x = "/OAuth/{}".format(session.get('Token'))
           return redirect(x)
    except:
            return redirect('/index')
    session['Page'] = "index"
    return redirect('/index')
def index():  # put application's code here
    session['Page'] = "index"
    return make_response(render_template('index.html', Title="Welcome Page"))
def k(Any_Word):
    if Any_Word == "Sign_Up" :
        return redirect(url_for('Sign_Up'))
    if Any_Word == "login" :
        return redirect(url_for('login'))
    if session.get('Token') != None and Any_Word != "Sign_Up" and Any_Word != "login":
        x = "/OAuth/{}".format(session.get('Token'))
        try :
           return redirect(x)
        except :
           return redirect(url_for('index'))
    session['Page'] = "index"
    return redirect(url_for('index'))
def ReturnToken():
    Email = request.form.get('email')
    Password = request.form.get('password')
    try:
        T=User.query.filter_by(email=Email).first()
        if T.password == Password :
            session['Task_Done'] = "GET ACCESS TOKEN SUCCESSFULLY"
            return make_response(jsonify({"Access Token" : T.Access_Token }),200)
    except:
        return make_response(jsonify({'Response':'wrong email or password'}),403)
    return make_response(jsonify({'Response':'wrong email or password'}),403)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
           N = User.query.filter_by(email=form.email.data)
           email = N[0].email
           password = N[0].password
           if form.email.data == email and form.password.data == password:
              flash('You have been logged in!', 'success')
              x = "/OAuth/{}".format(N[0].Access_Token)
              return redirect(x)
        except :
             flash('Login Unsuccessful. Please check username and password', 'danger')
    return make_response(render_template('Login.html', form=form, Title="Login"))
def log_out():
    session['Task_Done'] = "Logged out"
    New_Transaction = History(Access_Token=session.get('Token'), Creation_Date=datetime.utcnow(), Method_Used=request.method,
                              Task_Done=session.get('Task_Done'))
    db.session.add(New_Transaction)
    db.session.commit()
    session['Token'] = None
    return redirect('/')
def admin():
    session['Token'] = "Admin"
    form = Admin_Login()
    if form.validate_on_submit():
        if form.password.data == app.config.get('SECRET_KEY'):
            session['Page'] = 'Admin'
            Users = User.query.all()
            Cost = Annual_Cost_Per_Student.query.all()
            N_Student_Per_University_Table = N_Student_Per_University.query.all()
            Sucess_Dropout_Rates = rates.query.all()
            PV = Private_Vs_Public.query.all()
            HS = History.query.all()
            session['Task_Done'] = "Get Access to admin Dashboard"
            return render_template('Dashboard.html', Authenticated=True, username='Admin', Users=Users,N_Student_Per_University_Table=N_Student_Per_University_Table,Sucess_Dropout_Rates=Sucess_Dropout_Rates, Cost=Cost, PV=PV,History=HS)
        else:
            flash("Try to put a valid secret key")
    return make_response(render_template('admin.html', form=form))
def Sign_Up():
    form = RegistrationForm()
    session['Page'] = "Sign_Up"
    if form.validate_on_submit():
        token = jwt.encode({'username': form.username.data, 'email': form.email.data,'password': form.password.data,'exp':datetime.utcnow()+timedelta(days=180)}, app.config['SECRET_KEY'], algorithm="HS256")
        now = "{}".format(datetime.utcnow())
        New_User = User(username=form.username.data, email=form.email.data, password=form.password.data,Access_Token=token, Creation_Date=now)
        db.session.add(New_User)
        db.session.commit()
        flash("Account created successfully")
        return redirect(url_for('login'))
    return make_response(render_template('Sign_Up.html', form=form, Title="Sign_Up"))
@token_required
def list_of_universities(current_user):
    session['Task_Done'] = "Getting the list of universities"
    List = [university.University_Name.strip() for unviversity in N_Student_Per_University.query.all()]
    session['Task_Done'] = "View List of Universtites"
    return jsonify({'List of tunisian univeristies': List})
@token_required
def Get_Universiy_Data(current_user,Univ):
    session['Task_Done'] = "Getting Information about a specific university"
    List = [university.University_Name.strip() for university in N_Student_Per_University.query.all()]
    try :
        if Univ in List:
           for item in N_Student_Per_University.query.all():
              if item.University_Name == Univ:
                 Selected_University = item
                 session['Task_Done'] = f"View the data of a specific university {Univ}"

        return jsonify({Univ: [{"2014_2015": Selected_University.N_2014_2015},{"2015_2016": Selected_University.N_2015_2016},{"2016_2017": Selected_University.N_2016_2017},{"2017_2018": Selected_University.N_2017_2018},{"2018_2019": Selected_University.N_2018_2019},{"2019_2020": Selected_University.N_2019_2020}]})
    except:
       return jsonify({"response": "Put valid university name"})
@token_required
def List_Rates(current_user):
    try :
        l =[x.Status for x in rates.query.all()]
        session['Task_Done'] = "View Rates List"
        return jsonify({"List of rates": l})
    except:
        session['Task_Done'] = "failed to get the list of rates"
        return jsonify({"Response":"Failed to get the list of rates"})
@token_required
def Get_Rates_Of_Specidifc_Status(current_user,status):
    for item in rates.query.all():
        if item.Status == status:
            Row=item
            try:
                session['Task_Done'] = f"View the data of a specific rates {status}"
                return jsonify({status: [{"2014_2015": Row.N_2014_2015}, {"2015_2016": Row.N_2015_2016},{"2016_2017": Row.N_2016_2017}, {"2017_2018": Row.N_2017_2018},{"2018_2019": Row.N_2018_2019}, {"2019_2020": Row.N_2019_2020}]})
            except:
                session['Task_Done'] = "failed to get The data of a specific university"
                return make_response(jsonify({'Response': 'Wrong Try to put the right status'}))
    return make_response(jsonify({'Response': 'Wrong Try to put the right status'}))
@token_required
def specific(current_user,status, year1, year2):
    for item in rates.query.all():
        if item.Status == status:
            Row = item
            try:
                session['Task_Done'] = "Getting Access to status statistics within a specific period of time"
                return jsonify({status: {f"{year1}_{year2}": Row.__getattribute__(f'N_{year1}_{year2}')}})
            except:
                session['Task_Done'] = "failed to get of a specific status within a specified period of time"
                return make_response(jsonify({ 'Response': 'Wrong try to put two successive years separated by - take in consideration that data is gathered between 2014 and 2015'}))

    return make_response(jsonify({'Response': 'Wrong try to put two successive years separated by - take in consideration that data was gathered between 2014 and 2020'}))
@token_required
def Cost(current_user):
    session['Task_Done'] = "Getting Access to total cost per student statistics within a specific period of time"
    D = Annual_Cost_Per_Student.query.all()[0]
    return jsonify({"Total expenditures": [{"2014_2015": f'{D.N_2014_2015} TND'},{"2015_2016": f'{D.N_2015_2016} TND'},{"2016_2017": f'{D.N_2016_2017} TND'},{"2017_2018": f'{D.N_2017_2018} TND'},{"2018_2019": f'{D.N_2018_2019} TND'}]})
@token_required
def CostPerStudent(current_user, year1, year2):
    D = Annual_Cost_Per_Student.query.all()[0]
    Period = f"{year1}_{year2}"
    Period_To_Put_In = "N_" + Period
    try:
        Specified_Cost = f"{D.__getattribute__(Period_To_Put_In)}"
        session['Task_Done'] = "Getting Access to total cost per student statistics within a specific period of time"
        return jsonify({"Total expenditures": [{Period: f"{Specified_Cost} TND"}]})
    except:
        session['Task_Done'] = "Getting Access to total cost per student statistics within a specific period of time Unsucessfully"
        return jsonify({"Response": "Try to verify that years are consecutive and separated by - from 2014 to 2019"})
@token_required
def Get_Total_Number_Of_Students(current_user):
    X=Private_Vs_Public.query.all()[0]
    session['Task_Done'] = "View Total number of students"
    return jsonify({"Total Number of students(Public & Private)": [{"2014_2015": X.N_2014_2015},{"2015_2016": X.N_2015_2016},{"2016_2017": X.N_2016_2017},{"2017_2018": X.N_2017_2018},{"2018_2019": X.N_2018_2019},{"2019_2020": X.N_2019_2020}]})
@token_required
def Get_Number(current_user):
    session['Task_Done'] = "Getting Access to Proportion of students in the private sector in relation to total student"
    X= Private_Vs_Public.query.all()[1]
    return jsonify({"Proportion of students in the private sector in relation to total student	": [{"2014_2015": X.N_2014_2015},{"2015_2016": X.N_2015_2016},{"2016_2017": X.N_2016_2017},{"2017_2018": X.N_2017_2018},{"2018_2019": X.N_2018_2019},{"2019_2020": X.N_2019_2020}]})
@token_required
def Get_Number_Per_100(current_user):
    X= Private_Vs_Public.query.all()[2]
    session['Task_Done'] = "View N-of-Stu-per-100-inhabitant"
    return jsonify({"Number of students per 100 thousand inhabitants": [{"2014_2015": X.N_2014_2015},{"2015_2016": X.N_2015_2016},{"2016_2017": X.N_2016_2017},{"2017_2018": X.N_2017_2018},{"2018_2019": X.N_2018_2019},{"2019_2020": X.N_2019_2020}]})
def DeleteUser():
    email = request.args.get('email')
    try:
       User.query.filter_by(email=email).delete()
       db.session.commit()
       session['Task_Done'] = f"The Admin deleted the user whose email is {email}"
       return jsonify({"Response": "User Deleted Sucessfully"})
    except:
       return jsonify({"Response": "Something went wrong User is not deleted"})
def Manipulate_data(Univ):
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')
    New_Stat = request.args.get('New_Stat')
    try :
        N_Student_Per_University.query.filter_by(University_Name=Univ).first().__setattr__(f"N_{year1}_{year2}",New_Stat)
        db.session.commit()
        session['Task_Done'] = "Someone tried to login to the Admin Panel"
        return jsonify({"response":"Item modified Sucessfully"})
    except :
        return jsonify({"Response":"Something went wrong"})
def Manipulate_data_2(Rates_N):
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')
    New_Stat = request.args.get('New_Stat')
    try :
        rates.query.filter_by(Status=Rates_N).first().__setattr__(f"N_{year1}_{year2}",New_Stat)
        db.session.commit()
        session['Task_Done'] = "Getting Access to a specified status satatitics"
        return jsonify({"response":"Item modified Sucessfully"})
    except :
        return jsonify({"Response":"Something went wrong"})