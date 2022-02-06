from app import db
class History(db.Model):
    Transaction_ID = db.Column(db.Integer, primary_key= True, unique=True, nullable=False, autoincrement=True)
    Access_Token = db.Column(db.String(20), unique=False, nullable=True)
    Creation_Date = db.Column(db.String(120), nullable=True)
    Method_Used = db.Column(db.String(20), unique=False, nullable=True)
    Task_Done = db.Column(db.String(20), unique=False, nullable=True)

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
    Status = db.Column(db.String(20), nullable=True,default="Not verified")