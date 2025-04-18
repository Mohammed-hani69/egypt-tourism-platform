from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from models import User
from flask_babel import gettext as _


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
                                     
    # User type selection
    is_guide = BooleanField('Register as Tour Guide')
    is_student = BooleanField('Register as Language Student')
    is_tourist = BooleanField('Register as Tourist')
    
    # Basic information for all users
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    
    # Additional fields for non-tourists (guide/student)
    governorate = StringField('Governorate', validators=[Length(max=100)])
    city = StringField('City', validators=[Length(max=100)])
    education_level = SelectField('Education Level', 
                                 choices=[('', 'Select Education Level'),
                                         ('high_school', 'High School'),
                                         ('bachelor', 'Bachelor Degree'),
                                         ('master', 'Master Degree'),
                                         ('phd', 'PhD')],
                                 validators=[])
    university = StringField('University', validators=[Length(max=200)])
    
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
    languages = SelectMultipleField(_('اللغات'),
        choices=[
            ('ar', _('العربية')),
            ('en', _('الإنجليزية')),
            ('fr', _('الفرنسية')),
            ('de', _('الألمانية')),
            ('es', _('الإسبانية')),
            ('it', _('الإيطالية')),
            ('ru', _('الروسية')),
            ('zh', _('الصينية'))
        ],
        validators=[DataRequired()],
        description=_('اختر اللغات التي تجيدها'))
    specialization = StringField(_('التخصص'),
                            description=_('مثال: الآثار الفرعونية، التاريخ الإسلامي'))
    years_experience = IntegerField(_('سنوات الخبرة'),
                                  validators=[DataRequired(), NumberRange(min=0)])
    certification = StringField(_('الشهادات'),
                              description=_('مثال: شهادة الإرشاد السياحي المعتمدة'))
    submit = SubmitField(_('حفظ المعلومات'))


class GuideLanguageForm(FlaskForm):
    languages = StringField('Languages',
                          validators=[DataRequired()],
                          description='Separate languages with commas (e.g. Arabic, English, French)')
    submit = SubmitField('Save Languages')


class LanguagePracticeForm(FlaskForm):
    language = SelectField('Language', 
                          choices=[('ar', _('العربية')),
                                    ('en', _('الإنجليزية')),
                                    ('fr', _('الفرنسية')),
                                    ('de', _('الألمانية')),
                                    ('es', _('الإسبانية')),
                                    ('it', _('الإيطالية')),
                                    ('ru', _('الروسية')),
                                    ('zh', _('الصينية'))],
                          validators=[DataRequired()])
    proficiency_level = SelectField('Proficiency Level',
                                   choices=[('Beginner', 'Beginner'), 
                                           ('Intermediate', 'Intermediate'),
                                           ('Advanced', 'Advanced')],
                                   validators=[DataRequired()])
    availability = StringField('Availability', validators=[DataRequired()])
    interests = StringField('Interests')
    learning_goal = TextAreaField('Learning Goal')
    submit = SubmitField('Update Language Practice Profile')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    governorate = StringField('Governorate', validators=[Length(max=100)])
    city = StringField('City', validators=[Length(max=100)])
    education_level = SelectField('Education Level', 
                                choices=[('', 'Select Education Level'),
                                        ('high_school', 'High School'),
                                        ('bachelor', 'Bachelor Degree'),
                                        ('master', 'Master Degree'),
                                        ('phd', 'PhD')])
    university = StringField('University', validators=[Length(max=200)])
    bio = TextAreaField('Bio')
    profile_pic = StringField('Profile Picture URL', validators=[Length(max=200)])
    submit = SubmitField('Update Profile')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken. Please choose a different one.')
                
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please use a different one.')


class ChatGroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    language = SelectField('Language', 
                          choices=[('ar', _('العربية')),
                                    ('en', _('الإنجليزية')),
                                    ('fr', _('الفرنسية')),
                                    ('de', _('الألمانية')),
                                    ('es', _('الإسبانية')),
                                    ('it', _('الإيطالية')),
                                    ('ru', _('الروسية')),
                                    ('zh', _('الصينية'))],
                          validators=[DataRequired()])
    submit = SubmitField('Create Chat Group')


class ChatMessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


class SelectGuideForm(FlaskForm):
    guide_id = SelectField('Select Guide', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Select Guide')


class TourPlanForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    title_ar = StringField('Title (Arabic)', validators=[Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    description_ar = TextAreaField('Description (Arabic)')
    duration = IntegerField('Duration (days)', validators=[DataRequired(), NumberRange(min=1)])
    price = IntegerField('Price (EGP)', validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField('Image URL')
    submit = SubmitField('Create Tour Plan')


class TourPlanDestinationForm(FlaskForm):
    attraction_id = SelectField('Attraction', coerce=int, validators=[DataRequired()])
    day_number = IntegerField('Day Number', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField('Description')
    description_ar = TextAreaField('Description (Arabic)')
    submit = SubmitField('Add Destination')


class TourBookingForm(FlaskForm):
    start_date = StringField('Start Date', validators=[DataRequired()])
    number_of_people = IntegerField('Number of People', validators=[DataRequired(), NumberRange(min=1)])
    notes = TextAreaField('Additional Notes')
    submit = SubmitField('Book Tour')


class AssignGuideForm(FlaskForm):
    guide_id = SelectField('Select Guide', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Guide')


class TourProgressForm(FlaskForm):
    progress_percentage = IntegerField('Progress Percentage', 
        validators=[DataRequired(), NumberRange(min=0, max=100)])
    current_location = StringField('Current Location',
        validators=[DataRequired()])
    visited_attractions = TextAreaField('Visited Attractions')
    notes = TextAreaField('Notes')
    submit = SubmitField('Update Progress')


class TourPhotoForm(FlaskForm):
    image_url = StringField('Image URL', validators=[DataRequired()])
    caption = StringField('Caption', validators=[Length(max=200)])
    submit = SubmitField('Add Photo')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
