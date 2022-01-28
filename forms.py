from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Admin_Login(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class N_Student_Per_University_Reg(FlaskForm):
    University_Name = StringField('University_Name',validators=[DataRequired()])
    N_2014_2015 = StringField('N_2014_2015',validators=[DataRequired()])
    N_2015_2016 = StringField('N_2014_2015',validators=[DataRequired()])
    N_2016_2017 = StringField('N_2014_2015',validators=[DataRequired()])
    N_2017_2018 = StringField('N_2014_2015',validators=[DataRequired()])
    N_2018_2019 = StringField('N_2014_2015',validators=[DataRequired()])
    N_2019_2020 = StringField('N_2014_2015',validators=[DataRequired()])
    submit = SubmitField('submit')

