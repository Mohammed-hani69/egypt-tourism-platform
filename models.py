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
    is_tourist = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
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
    guide_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    language = db.Column(db.String(50), nullable=False)
    proficiency_level = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.String(200), nullable=True)
    interests = db.Column(db.String(200), nullable=True)
    
    # Relationship to access the student details
    student = db.relationship('User', foreign_keys=[student_id], backref=db.backref('language_practice', uselist=False))
    guide = db.relationship('User', foreign_keys=[guide_id], backref=db.backref('students', lazy='dynamic'))
    
    
class ChatGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    guide_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    
    # Relationships
    guide = db.relationship('User', backref=db.backref('chat_groups', lazy='dynamic'))
    messages = db.relationship('ChatMessage', backref='chat_group', lazy='dynamic', cascade='all, delete-orphan')
    members = db.relationship('ChatGroupMember', backref='chat_group', lazy='dynamic', cascade='all, delete-orphan')


class ChatGroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_group_id = db.Column(db.Integer, db.ForeignKey('chat_group.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('chat_memberships', lazy='dynamic'))
    
    # Ensure a user can only be a member of a chat group once
    __table_args__ = (db.UniqueConstraint('user_id', 'chat_group_id'),)


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_group_id = db.Column(db.Integer, db.ForeignKey('chat_group.id'), nullable=False)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('chat_messages', lazy='dynamic'))


class TourPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    title_ar = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)
    description_ar = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False)  # Duration in days
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200), nullable=True)
    
    # Relationships
    destinations = db.relationship('TourPlanDestination', backref='tour_plan', lazy='dynamic', cascade='all, delete-orphan')
    bookings = db.relationship('TourBooking', backref='tour_plan', lazy='dynamic')


class TourPlanDestination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_plan_id = db.Column(db.Integer, db.ForeignKey('tour_plan.id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction.id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    description_ar = db.Column(db.Text, nullable=True)
    
    # Relationship
    attraction = db.relationship('Attraction')
    
    # Ensure a destination appears only once in a tour plan
    __table_args__ = (db.UniqueConstraint('tour_plan_id', 'attraction_id', 'day_number'),)


class TourBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tourist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tour_plan_id = db.Column(db.Integer, db.ForeignKey('tour_plan.id'), nullable=False)
    guide_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tourist = db.relationship('User', foreign_keys=[tourist_id], backref=db.backref('tour_bookings', lazy='dynamic'))
    guide = db.relationship('User', foreign_keys=[guide_id], backref=db.backref('guided_tours', lazy='dynamic'))
    progress = db.relationship('TourProgress', backref='booking', lazy='dynamic', cascade='all, delete-orphan')


class TourProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('tour_booking.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('tour_plan_destination.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationship
    destination = db.relationship('TourPlanDestination')
    photos = db.relationship('TourPhoto', backref='progress', lazy='dynamic', cascade='all, delete-orphan')
    
    # Ensure a destination is only tracked once per booking
    __table_args__ = (db.UniqueConstraint('booking_id', 'destination_id'),)


class TourPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    progress_id = db.Column(db.Integer, db.ForeignKey('tour_progress.id'), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(200), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
