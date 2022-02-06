from flask import Flask, session, request ,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import random

from datetime import datetime
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TU.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'street.cherk@gmail.com'
app.config['MAIL_PASSWORD'] = '54811289Rami'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

from models.model import History, Private_Vs_Public , N_Student_Per_University , Annual_Cost_Per_Student , rates , User
from routes.routes import CostPerStudent , Get_Total_Number_Of_Students , Get_Number , Get_Number_Per_100 , Manipulate_data , Get_Rates_Of_Specidifc_Status , specific , Cost , DeleteUser , Manipulate_data_2 , OAuth, Main , index , k , ReturnToken , login , log_out , Sign_Up , list_of_universities , Get_Universiy_Data , List_Rates , admin

app.add_url_rule('/OAuth/<string:Token>', view_func=OAuth, methods=['GET', 'POST'])
app.add_url_rule('/', view_func=Main, methods=['GET', 'POST'])
app.add_url_rule('/index', view_func=index, methods=['GET', 'POST'])
app.add_url_rule('/<string:Any_Word>', view_func=k,  methods=['GET', 'POST'])
app.add_url_rule('/GetToken', view_func=ReturnToken,  methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=login,  methods=['GET', 'POST'])
app.add_url_rule('/log_out', view_func=log_out,  methods=['POST'])
app.add_url_rule('/Sign_Up', view_func=Sign_Up,  methods=['GET', 'POST'])
app.add_url_rule('/user/list_of_universities', view_func=list_of_universities,  methods=['GET'])
app.add_url_rule('/user/list_of_universities/<string:Univ>', view_func=Get_Universiy_Data,  methods=['GET'])
app.add_url_rule('/user/rates', view_func=List_Rates,  methods=['GET'])
app.add_url_rule('/user/rates/<string:status>', view_func=Get_Rates_Of_Specidifc_Status,  methods=['GET'])
app.add_url_rule('/user/rates/<string:status>/<string:year1>-<string:year2>', view_func=specific,  methods=['GET'])
app.add_url_rule('/user/total_Cost_per_student', view_func=Cost,  methods=['GET'])
app.add_url_rule('/user/total_Cost_per_student/<string:year1>-<string:year2>', view_func=CostPerStudent,  methods=['GET'])
app.add_url_rule('/user/Total_Number_Of_Student', view_func=Get_Total_Number_Of_Students,  methods=['GET'])
app.add_url_rule('/user/Prop-private-total-student', view_func=Get_Number,  methods=['GET'])
app.add_url_rule('/user/N-Of-Stu-per-100-student', view_func=Get_Number_Per_100,  methods=['GET'])
app.add_url_rule('/admin', view_func=admin,  methods=['GET', 'POST'])
app.add_url_rule('/admin/users/delete', view_func=DeleteUser,  methods=['DELETE'])
app.add_url_rule('/admin/<string:Univ>', view_func=Manipulate_data,  methods=['PUT'])
app.add_url_rule('/admin/rates/<string:Rates_N>', view_func=Manipulate_data_2,  methods=['PUT'])
app.add_url_rule('/verified_email',view_func=Verified_Email,methods=['POST'])

@app.route('/Confirmation',methods=['POST'])
def Send_Confirmation_Code():
    msg = Message('Email Confirmation ', sender=('TU API','street.cherk@gmail.com') , recipients=[session.get('email')])
    msg.html = render_template('Email_Confirmation.html',username=session.get('username'),Verification_Code=session.get('Verification_Code'))
    mail.send(msg)
    return ''


@app.after_request
def after_request_func(response):
  Final_Token = session.get('Token')
  if session.get('Task_Done') == None:
     session['Task_Done'] = ""
  if session.get('Token') == None:
     Final_Token = "Visitor"
  X = History.query.all()[-1]
  if X.Task_Done != session.get('Task_Done') :
     New_Transaction = History(Access_Token=Final_Token, Creation_Date = datetime.utcnow(), Method_Used=request.method, Task_Done=session.get('Task_Done'))
     db.session.add(New_Transaction)
     db.session.commit()
  return response

@app.before_first_request
def before_first_request_func():
    Final_Token = session.get('Token')
    if session.get('Task_Done') == None:
        session['Task_Done'] = ""
    if session.get('Token') == None:
        Final_Token = "Visitor"
    if session.get('Task_Done') == "Logged out" :
        New_Transaction = History(Access_Token=Final_Token, Creation_Date=datetime.utcnow(), Method_Used=request.method,Task_Done=session.get('Task_Done'))
        db.session.add(New_Transaction)
        db.session.commit()



if __name__ == '__main__':
  app.run(debug=True, use_debugger=True, use_reloader=True)
