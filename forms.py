from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    is_guide = BooleanField('Register as Tour Guide')
    is_student = BooleanField('Register as Language Student')
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Review', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), 
                                           (4, '4 Stars'), (5, '5 Stars')], 
                         validators=[DataRequired()], coerce=int)
    submit = SubmitField('Submit Review')


class GuideForm(FlaskForm):
    languages = StringField('Languages (comma separated)', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    phone = StringField('Contact Phone', validators=[DataRequired()])
    years_experience = IntegerField('Years of Experience', validators=[NumberRange(min=0)])
    specialization = StringField('Specialization')
    certification = StringField('Certification')
    submit = SubmitField('Update Guide Profile')


class LanguagePracticeForm(FlaskForm):
    language = SelectField('Language', 
                          choices=[('English', 'English'), ('Arabic', 'Arabic'), 
                                   ('French', 'French'), ('German', 'German'),
                                   ('Spanish', 'Spanish'), ('Italian', 'Italian'),
                                   ('Russian', 'Russian'), ('Chinese', 'Chinese')],
                          validators=[DataRequired()])
    proficiency_level = SelectField('Proficiency Level',
                                   choices=[('Beginner', 'Beginner'), 
                                           ('Intermediate', 'Intermediate'),
                                           ('Advanced', 'Advanced')],
                                   validators=[DataRequired()])
    availability = StringField('Availability', validators=[DataRequired()])
    interests = StringField('Interests')
    submit = SubmitField('Update Language Practice Profile')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
