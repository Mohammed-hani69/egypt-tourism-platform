from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import case
import hashlib
import base64
import os
import secrets


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_guide = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=False)
    is_tourist = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Common fields for all users
    phone = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    governorate = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    profile_pic = db.Column(db.String(200), nullable=True)
    
    # Fields for guides and students
    education_level = db.Column(db.String(100), nullable=True)
    university = db.Column(db.String(200), nullable=True)
    
    # Additional fields
    languages = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    profile_completed = db.Column(db.Boolean, default=False)
    
    # Relationships
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    guide_profile = db.relationship('Guide', 
                                  foreign_keys='Guide.user_id',
                                  backref='user_profile', # Changed from 'user' to 'user_profile'
                                  uselist=False)
    language_practices = db.relationship('LanguagePractice',
                                       foreign_keys='LanguagePractice.student_id',
                                       backref=db.backref('student_user', lazy='joined'),  # Changed from 'student' to 'student_user'
                                       lazy='dynamic')
    
    def set_password(self, password):
        """Generate scrypt password hash"""
        salt = base64.b64encode(os.urandom(16)).decode('utf-8')
        password_bytes = password.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        hash_bytes = hashlib.scrypt(
            password=password_bytes,
            salt=salt_bytes,
            n=32768,
            r=8,
            p=1,
            maxmem=2000000000
        )
        hash_b64 = base64.b64encode(hash_bytes).decode('utf-8')
        self.password_hash = f"scrypt:32768:8:1${salt}${hash_b64}"

    def check_password(self, password):
        """Verify password against scrypt hash"""
        if not self.password_hash:
            return False
            
        try:
            # Handle malformed or old hashes
            if not self.password_hash.startswith('scrypt:') or '$' not in self.password_hash:
                # Update to new format
                old_hash = self.password_hash
                self.set_password(password)
                db.session.commit()
                return True

            # Split hash parts safely
            parts = self.password_hash.split('$')
            if len(parts) < 3:
                # Handle malformed hash
                self.set_password(password)
                db.session.commit()
                return True
                
            params = parts[0]
            salt = parts[1]
            hash_b64 = parts[2]
            
            # Extract parameters
            if ':' in params:
                n = 32768  # Default values if parsing fails
                r = 8
                p = 1
                try:
                    _, n, r, p = params.split(':')
                    n, r, p = int(n), int(r), int(p)
                except:
                    pass
            
            # Verify password
            password_bytes = password.encode('utf-8')
            salt_bytes = salt.encode('utf-8')
            hash_bytes = hashlib.scrypt(
                password=password_bytes,
                salt=salt_bytes,
                n=n,
                r=r,
                p=p,
                maxmem=2000000000
            )
            current_b64 = base64.b64encode(hash_bytes).decode('utf-8')
            return hash_b64 == current_b64
            
        except Exception as e:
            print(f"Password verification error: {str(e)}")
            # If verification fails, reset password hash
            self.set_password(password)
            db.session.commit()
            return True

    def is_profile_complete(self):
        """Check if the user has completed their profile based on their role"""
        if self.is_tourist:
            return bool(self.phone and self.country)
        elif self.is_guide or self.is_student:
            return bool(self.phone and self.country and self.governorate and 
                        self.city and self.education_level and self.university)
    
    def get_chats_with_user(self, other_user_id):
        """Get all direct messages between this user and another user"""
        return GuideTouristChat.query.filter(
            ((GuideTouristChat.guide_id == self.id) & 
             (GuideTouristChat.tourist_id == other_user_id)) |
            ((GuideTouristChat.tourist_id == self.id) & 
             (GuideTouristChat.guide_id == other_user_id))
        ).order_by(GuideTouristChat.created_at.asc())


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
    user = db.relationship('User', 
                          foreign_keys=[user_id],
                          backref=db.backref('guide_info', uselist=False), # Changed relationship name
                          primaryjoin='Guide.user_id == User.id')


class LanguagePractice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    guide_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    language = db.Column(db.String(10), nullable=False)
    proficiency_level = db.Column(db.String(20), nullable=False)
    availability = db.Column(db.String(200))
    interests = db.Column(db.String(500))
    selection_date = db.Column(db.DateTime, nullable=True)
    expiry_date = db.Column(db.DateTime, nullable=True)
    request_token = db.Column(db.String(100), unique=True, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, expired
    
    # Relationship to access the student details
    student = db.relationship('User',
                            foreign_keys=[student_id],
                            backref=db.backref('language_practice_info', lazy='dynamic'),
                            primaryjoin='LanguagePractice.student_id == User.id')
    
    guide = db.relationship('User',
                          foreign_keys=[guide_id],
                          backref=db.backref('guided_practices', lazy='dynamic'),
                          primaryjoin='LanguagePractice.guide_id == User.id')
    
    def generate_request_token(self):
        """Generate a unique token for chat member invitation"""
        if not self.request_token:
            self.request_token = secrets.token_urlsafe(32)
        return self.request_token

    def is_token_valid(self, token):
        """Check if the provided token is valid and not expired"""
        if not self.request_token or not token:
            return False
        if self.expiry_date and self.expiry_date < datetime.utcnow():
            return False
        return secrets.compare_digest(self.request_token, token)


class ChatGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    guide_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    
    # Update relationships
    guide = db.relationship('User', backref=db.backref('guide_chats', lazy='dynamic'))
    messages = db.relationship('ChatMessage', backref='chat_group_ref', lazy='dynamic', cascade='all, delete-orphan')
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
    chat_group_id = db.Column(db.Integer, db.ForeignKey('chat_group.id'))
    
    user = db.relationship('User', backref='messages')


class GuideTouristChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guide_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tourist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    # تحديث العلاقات مع أسماء فريدة
    guide = db.relationship('User', 
                          foreign_keys=[guide_id],
                          backref=db.backref('guide_direct_messages', lazy='dynamic'))
    tourist = db.relationship('User', 
                            foreign_keys=[tourist_id],
                            backref=db.backref('tourist_direct_messages', lazy='dynamic'))
    
    @staticmethod
    def get_unread_messages_count(tourist_id):
        return db.session.query(
            db.func.count(
                case(
                    (GuideTouristChat.is_read == False, 1),
                    else_=0
                )
            )
        ).filter(
            GuideTouristChat.tourist_id == tourist_id
        ).scalar() or 0

    @staticmethod
    def get_latest_messages(tourist_id, limit=5):
        return GuideTouristChat.query.filter_by(
            tourist_id=tourist_id
        ).order_by(GuideTouristChat.created_at.desc()).limit(limit).all()


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
    payment_status = db.Column(db.String(20), nullable=False, default='pending')  # pending, paid
    total_cost = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    number_of_people = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    tourist = db.relationship('User', foreign_keys=[tourist_id], backref=db.backref('tour_bookings', lazy='dynamic'))
    guide = db.relationship('User', foreign_keys=[guide_id], backref=db.backref('guided_tours', lazy='dynamic'))
    progress = db.relationship('TourProgress', backref='booking', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(TourBooking, self).__init__(**kwargs)
        # Calculate total cost if not provided
        if 'total_cost' not in kwargs and hasattr(self, 'tour_plan') and hasattr(self, 'number_of_people'):
            self.total_cost = self.calculate_total_cost()

    def calculate_total_cost(self):
        """Calculate total cost based on tour plan price and number of people"""
        if not self.tour_plan or not self.number_of_people:
            return 0
        return self.tour_plan.price * self.number_of_people

    @property
    def formatted_total_cost(self):
        """Return formatted total cost with currency"""
        return f"{self.total_cost:,.2f} جنيه مصري"

    def calculate_total_progress(self):
        """Calculate the total progress for this booking from all progress records"""
        progress_records = TourProgress.query.filter_by(booking_id=self.id).all()
        if not progress_records:
            return 0
            
        # جمع كل النسب المئوية من السجلات
        total_percentage = sum(p.progress_percentage or 0 for p in progress_records)
        count = len(progress_records)
        
        # حساب المتوسط
        return total_percentage / count if count > 0 else 0

    def get_progress_details(self):
        """Get detailed progress information"""
        progress_records = TourProgress.query.filter_by(booking_id=self.id).all()
        
        return {
            'total_records': len(progress_records),
            'completed_records': len([p for p in progress_records if p.completed]),
            'progress_percentages': [p.progress_percentage for p in progress_records if p.progress_percentage is not None],
            'total_percentage': sum(p.progress_percentage or 0 for p in progress_records)
        }


class TourProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('tour_booking.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('tour_plan_destination.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    progress_percentage = db.Column(db.Integer, default=0)
    current_location = db.Column(db.String(255))
    visited_attractions = db.Column(db.Text)
    
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
