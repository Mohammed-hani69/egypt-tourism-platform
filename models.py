from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_guide = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=False)
    languages = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(200), nullable=True)
    
    # Relationships
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    description_ar = db.Column(db.Text, nullable=True)
    
    # Relationships
    attractions = db.relationship('Attraction', backref='region', lazy='dynamic')


class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=False)
    description_ar = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    ticket_price = db.Column(db.String(100), nullable=True)
    opening_hours = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    featured = db.Column(db.Boolean, default=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    
    # Relationships
    reviews = db.relationship('Review', backref='attraction', lazy='dynamic')
    restaurants = db.relationship('Restaurant', backref='attraction', lazy='dynamic')
    activities = db.relationship('Activity', backref='attraction', lazy='dynamic')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction.id'), nullable=False)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    description_ar = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    cuisine_type = db.Column(db.String(100), nullable=True)
    price_range = db.Column(db.String(50), nullable=True)
    contact = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction.id'), nullable=False)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    description_ar = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    price = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction.id'), nullable=False)


class Guide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    years_experience = db.Column(db.Integer, nullable=True)
    specialization = db.Column(db.String(200), nullable=True)
    certification = db.Column(db.String(200), nullable=True)
    available = db.Column(db.Boolean, default=True)
    
    # Relationship to access the user details
    user = db.relationship('User', backref=db.backref('guide_profile', uselist=False))


class LanguagePractice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    proficiency_level = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.String(200), nullable=True)
    interests = db.Column(db.String(200), nullable=True)
    
    # Relationship to access the student details
    student = db.relationship('User', backref=db.backref('language_practice', uselist=False))
