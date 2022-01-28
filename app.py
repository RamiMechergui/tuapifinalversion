from forms import LoginForm,Admin_Login,N_Student_Per_University_Reg
from flask import Flask, render_template, url_for, flash, redirect, make_response, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta
from functools import wraps

# decorator for verifying the JWT

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TU.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
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
         return jsonify({
            'message' : 'Token is invalid'
         }), 401
      # returns the current logged in users contex to the routes
      return f(current_user, *args, **kwargs)

   return decorated
class History(db.Model):
    Transaction_ID = db.Column(db.Integer, primary_key= True, unique=True, nullable=False, autoincrement=True)
    Access_Token = db.Column(db.String(20), unique=False, nullable=True)
    Creation_Date = db.Column(db.String(120), nullable=True)
    Method_Used = db.Column(db.String(20), unique=False, nullable=True)
    Task_Done = db.Column(db.String(20), unique=False, nullable=True)

    def __repr__(self):
        return f"Transaction_ID : {self.Transaction_ID} Access_Token: {self.Access_Token} Creation_Date : {self.Creation_Date} :  Method_Used {self.Method_Used} Task_Done : {self.Task_Done} "
class Private_Vs_Public(db.Model):
    N = db.Column(db.String(35), primary_key=True, unique=True, nullable=False)
    N_2014_2015 = db.Column(db.String(20), unique=False, nullable=False)
    N_2015_2016 = db.Column(db.String(20), unique=False, nullable=False)
    N_2016_2017 = db.Column(db.String(20), unique=False, nullable=False)
    N_2017_2018 = db.Column(db.String(20), unique=False, nullable=False)
    N_2018_2019 = db.Column(db.String(20), unique=False, nullable=False)
    N_2019_2020 = db.Column(db.String(20), unique=False, nullable=False)
class Annual_Cost_Per_Student(db.Model):
    Total_Expenditure = db.Column(db.String(35), primary_key=True, unique=True, nullable=False)
    N_2014_2015 = db.Column(db.String(20), unique=False, nullable=False)
    N_2015_2016 = db.Column(db.String(20), unique=False, nullable=False)
    N_2016_2017 = db.Column(db.String(20), unique=False, nullable=False)
    N_2017_2018 = db.Column(db.String(20), unique=False, nullable=False)
    N_2018_2019 = db.Column(db.String(20), unique=False, nullable=False)
class N_Student_Per_University(db.Model):
    University_Name = db.Column(db.String(35), primary_key=True, unique=True, nullable=False)
    N_2014_2015 = db.Column(db.String(20), unique=False, nullable=False)
    N_2015_2016 = db.Column(db.String(20), unique=False, nullable=False)
    N_2016_2017 = db.Column(db.String(20), unique=False, nullable=False)
    N_2017_2018 = db.Column(db.String(20), unique=False, nullable=False)
    N_2018_2019 = db.Column(db.String(20), unique=False, nullable=False)
    N_2019_2020 = db.Column(db.String(20), unique=False, nullable=False)

class rates(db.Model):
    Status = db.Column(db.String(35), primary_key=True, unique=True, nullable=False)
    N_2014_2015 = db.Column(db.String(20), unique=False, nullable=False)
    N_2015_2016 = db.Column(db.String(20), unique=False, nullable=False)
    N_2016_2017 = db.Column(db.String(20), unique=False, nullable=False)
    N_2017_2018 = db.Column(db.String(20), unique=False, nullable=False)
    N_2018_2019 = db.Column(db.String(20), unique=False, nullable=False)
    N_2019_2020 = db.Column(db.String(20), unique=False, nullable=False)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    Access_Token = db.Column(db.String(20), unique=True, nullable=False)
    Creation_Date = db.Column(db.String(120), nullable=False)

@app.route('/OAuth/<string:Token>', methods=['GET', 'POST'])
def OAuth(Token):
    data = jwt.decode(Token, app.config['SECRET_KEY'], algorithms=["HS256"])
    try:
        email = data['email']
        password = data['password']
        N = User.query.filter_by(email=email)
        if N[0].email == email and N[0].password == password:
          session['Token'] = Token
          session['username'] = data['username']
          request.headers['x-access-token'] = Token
          M = [S for S in History.query.all() if S.Access_Token == session.get('Token')]
          HS = History.query.all()
          session['Task_Done'] = "Successfully Logged in"
          return make_response(render_template('index.html', Page="", Authenticated=True, id=N[0].id, username=N[0].username,M=M,access_token=N[0].Access_Token, password=N[0].password, Title=session.get('username'),History=HS))
    except :
            return make_response(redirect('/index'))

@app.route('/',methods=['GET','POST'])
def Main():
    if session.get('Token') != None :
        x = "/OAuth/{}".format(session.get('Token'))
        try :
            return redirect(x)
        except :
            return redirect('/index')
    session['Page'] = "index"
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():  # put application's code here
    session['Page'] = "index"
    return make_response(render_template('index.html', Title="Welcome Page"))

@app.route('/<string:Any_Word>',methods=['GET','POST'])
def k(Any_Word):
    if session.get('Token'):
        x = "/OAuth/{}".format(session.get('Token'))
        try :
           return redirect(x)
        except :
           return redirect('/index')
    session['Page'] = "index"
    return redirect('/index')

@app.route('/modification',methods=['GET','POST'])
def modif():
    db.session.query(rates).filter(rates.Status == "Sucess").update({rates.Status: "Success"})
    db.session.commit()
    return "done"

@app.route('/GetToken',methods=['GET','POST'])
def ReturnToken():
    Email = request.form.get('email')
    Password = request.form.get('password')
    try:
        T = User.query.filter_by(email=Email).first()
        if T.password == Password :
            session['Task_Done'] = "GET ACCESS TOKEN SUCCESSFULLY"
            return make_response(jsonify({"Access Token" : T.Access_Token }),200)
    except:
        return make_response(jsonify({'Response':'wrong email or password'}),403)
    return make_response(jsonify({'Response':'wrong email or password'}),403)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        N = User.query.filter_by(email=form.email.data)
        email = N[0].email
        password = N[0].password
        if form.email.data == email and form.password.data == password:
            flash('You have been logged in!', 'success')
            x = "/OAuth/{}".format(N[0].Access_Token)
            session['Task_Done'] = "Login Sucessfullyd"
            return redirect(x)
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return make_response(render_template('login.html', form=form, Title="Login"))

@app.route('/log_out', methods=['POST'])
def log_out():
    session['Task_Done'] = "Logged out"
    New_Transaction = History(Access_Token=session.get('Token'), Creation_Date=datetime.utcnow(), Method_Used=request.method,
                              Task_Done=session.get('Task_Done'))
    db.session.add(New_Transaction)
    db.session.commit()
    session['Token'] = None
    return redirect('/')

@app.route('/admin', methods=['GET', 'POST'])
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
            return render_template('Dashboard.html', Authenticated=True, username='Admin', Users=Users,
                                   N_Student_Per_University_Table=N_Student_Per_University_Table,
                                   Sucess_Dropout_Rates=Sucess_Dropout_Rates, Cost=Cost, PV=PV,History=HS)
        else:
            flash("Try to put a valid secret key")
    return make_response(render_template('admin.html', form=form))

@app.route('/Sign_Up', methods=['GET', 'POST'])
def Sign_Up():
    form = RegistrationForm()
    session['Page'] = "Sign_Up"
    if form.validate_on_submit():
        token = jwt.encode({'username': form.username.data, 'email': form.email.data, 'password': form.password.data,
                            'exp': datetime.utcnow() + timedelta(days=180)}, app.config['SECRET_KEY'],
                           algorithm="HS256")
        now = "{}".format(datetime.utcnow())
        New_User = User(username=form.username.data, email=form.email.data, password=form.password.data,
                        Access_Token=token, Creation_Date=now)
        db.session.add(New_User)
        db.session.commit()
        flash("Account created successfully")
        session['Task_Done'] = "Successfully Sign Up"
        return redirect(url_for('login', Title="Login"))
    return make_response(render_template('Sign_Up.html', form=form, Title="Sign_Up"))

@app.route('/user/list_of_universities', methods=['GET'])  # GET the list of Tunisian Universities
@token_required
def list_of_universities(current_user):
    session['Task_Done'] = "Getting the list of universities"
    List = [university.University_Name.strip() for unviversity in N_Student_Per_University.query.all()]
    session['Task_Done'] = "View List of Universtites"
    return jsonify({'List of tunisian univeristies': List})

@app.route('/user/list_of_universities/<string:Univ>', methods=['GET'])
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

@app.route('/user/rates')
@token_required
def List_Rates(current_user):
    try :
        l =[x.Status for x in rates.query.all()]
        session['Task_Done'] = "View Rates List"
        return jsonify({"List of rates": l})
    except:
        session['Task_Done'] = "failed to get the list of rates"
        return jsonify({"Response":"Failed to get the list of rates"})

@app.route('/user/rates/<string:status>')
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

@app.route('/user/rates/<string:status>/<string:year1>-<string:year2>', methods=['GET'])
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

@app.route('/user/total_Cost_per_student')
@token_required
def Cost(current_user):
    session['Task_Done'] = "Getting Access to total cost per student statistics within a specific period of time"
    D = Annual_Cost_Per_Student.query.all()[0]
    return jsonify({"Total expenditures": [{"2014_2015": f'{D.N_2014_2015} TND'},{"2015_2016": f'{D.N_2015_2016} TND'},{"2016_2017": f'{D.N_2016_2017} TND'},{"2017_2018": f'{D.N_2017_2018} TND'},{"2018_2019": f'{D.N_2018_2019} TND'}]})

@app.route('/user/total_Cost_per_student/<string:year1>-<string:year2>', methods=['GET'])
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

@app.route('/user/Total_Number_Of_Student',methods=['GET'])
@token_required
def Get_Total_Number_Of_Students(current_user):
    session['Task_Done'] = "Getting Access to total number of student statistics"
    X=Private_Vs_Public.query.all()[0]
    session['Task_Done'] = "View Total number of students"
    return jsonify({"Total Number of students(Public & Private)": [{"2014_2015": X.N_2014_2015},{"2015_2016": X.N_2015_2016},{"2016_2017": X.N_2016_2017},{"2017_2018": X.N_2017_2018},{"2018_2019": X.N_2018_2019},{"2019_2020": X.N_2019_2020}]})

@app.route('/user/Prop-private-total-student', methods=['GET'])
@token_required
def Get_Number(current_user):
    session['Task_Done'] = "Getting Access to Proportion of students in the private sector in relation to total student"
    X= Private_Vs_Public.query.all()[1]
    session['Task_Done'] = "View proportion of private student comparing to total students"
    return jsonify({"Proportion of students in the private sector in relation to total student	": [{"2014_2015": X.N_2014_2015},{"2015_2016": X.N_2015_2016},{"2016_2017": X.N_2016_2017},{"2017_2018": X.N_2017_2018},{"2018_2019": X.N_2018_2019},{"2019_2020": X.N_2019_2020}]})

@app.route('/user/N-Of-Stu-per-100-student', methods=['GET'])
@token_required
def Get_Number_Per_100(current_user):
    session['Task_Done'] = "View Students"
    X= Private_Vs_Public.query.all()[2]
    session['Task_Done'] = "View N-of-Stu-per-100-inhabitant"
    return jsonify({"Number of students per 100 thousand inhabitants": [{"2014_2015": X.N_2014_2015},{"2015_2016": X.N_2015_2016},{"2016_2017": X.N_2016_2017},{"2017_2018": X.N_2017_2018},{"2018_2019": X.N_2018_2019},{"2019_2020": X.N_2019_2020}]})

@app.route('/admin/users/delete',methods=['DELETE'])
def DeleteUser():
    email = request.args.get('email')
    try:
       User.query.filter_by(email=email).delete()
       db.session.commit()
       session['Task_Done'] = f"The Admin deleted the user whose email is {email}"
       return jsonify({"Response": "User Deleted Sucessfully"})
    except:
       return jsonify({"Response": "Something went wrong User is not deleted"})

@app.route('/admin/<string:Univ>',methods=['PUT'])
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

@app.route('/admin/rates/<string:Rates_N>',methods=['PUT'])
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

@app.after_request
def after_request_func(response):
    Final_Token = session.get('Token')
    if session.get('Task_Done') == None :
        session['Task_Done'] = ""
    if session.get('Token') == None :
        Final_Token = "Visitor"
    New_Transaction = History(Access_Token=Final_Token, Creation_Date = datetime.utcnow(),Method_Used=request.method, Task_Done=session.get('Task_Done'))
    db.session.add(New_Transaction)
    db.session.commit()
    return response

if __name__ == '__main__':
    app.run()
