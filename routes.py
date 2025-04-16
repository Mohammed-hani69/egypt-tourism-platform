from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session, g, abort, current_app, Response, stream_with_context
from werkzeug.urls import url_parse  # Updated import
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from extensions import db, babel
from flask_babel import gettext as _
from models import (User, Attraction, Region, Review, Restaurant, Activity, Guide, LanguagePractice,
                    ChatGroup, ChatGroupMember, ChatMessage, TourPlan, TourPlanDestination, 
                    TourBooking, TourProgress, TourPhoto, GuideTouristChat)
from forms import (RegistrationForm, LoginForm, ReviewForm, GuideForm, LanguagePracticeForm, SearchForm,
                   ChatGroupForm, ChatMessageForm, SelectGuideForm, TourPlanForm, TourPlanDestinationForm, 
                   TourBookingForm, AssignGuideForm, TourProgressForm, TourPhotoForm, ProfileForm, GuideLanguageForm)
from datetime import datetime, date, timedelta
from sqlalchemy import text, case
import os
import json
import time
from flask_wtf.csrf import CSRFProtect, validate_csrf
from wtforms.validators import ValidationError
from firebase_config import db_realtime, mark_message_as_read
import secrets
import stripe
from os import environ
from config import Config

# Update Stripe configuration
stripe.api_key = Config.STRIPE_SECRET_KEY

csrf = CSRFProtect()

# Create blueprint
main = Blueprint('main', __name__)

# Set up locale selector
def get_locale():
    # Try to get the language from the session
    if 'language' in session:
        return session['language']
    # Default to English
    return 'en'

def count_reviews_by_rating(reviews, rating):
    return sum(1 for review in reviews if review.rating == rating)

@main.before_app_request
def before_request():
    g.locale = str(get_locale())
    g.search_form = SearchForm()
    g.count_reviews_by_rating = count_reviews_by_rating

# Replace all @app decorators with @main decorators
@main.route('/set_language/<language>')
def set_language(language):
    session['language'] = language
    return redirect(request.referrer or url_for('main.index'))

@main.route('/')
def index():
    # Get featured attractions
    featured_attractions = Attraction.query.filter_by(featured=True).limit(4).all()

    # Get all regions for the navigation
    regions = Region.query.all()

    # Get active tour plans
    tour_plans = TourPlan.query\
        .order_by(TourPlan.created_at.desc())\
        .limit(6)\
        .all()

    return render_template('index.html', 
                           title='Home',
                           featured_attractions=featured_attractions,
                           regions=regions,
                           tour_plans=tour_plans)

@main.route('/attractions')
def attractions():
    # Get query parameters
    region_id = request.args.get('region', type=int)
    sort_by = request.args.get('sort', 'name')

    # Base query
    query = Attraction.query

    # Filter by region if provided
    if region_id:
        query = query.filter_by(region_id=region_id)

    # Sort results
    if sort_by == 'name':
        query = query.order_by(Attraction.name)
    elif sort_by == 'rating':
        # This is more complex and might require a subquery or join
        # For simplicity, we'll stick with name sorting for now
        query = query.order_by(Attraction.name)

    # Get all attractions based on filters
    attractions = query.all()

    # Get all regions for the filter dropdown
    regions = Region.query.all()

    return render_template('attractions.html', 
                           title='Attractions',
                           attractions=attractions,
                           regions=regions,
                           selected_region=region_id,
                           sort_by=sort_by)

@main.route('/attraction/<int:attraction_id>')
def attraction_detail(attraction_id):
    # Get the attraction details
    attraction = Attraction.query.get_or_404(attraction_id)

    # Get reviews with user info
    reviews = Review.query\
        .filter_by(attraction_id=attraction_id)\
        .order_by(Review.date_posted.desc())\
        .all()

    # Get nearby restaurants
    restaurants = Restaurant.query.filter_by(attraction_id=attraction_id).all()

    # Get available activities
    activities = Activity.query.filter_by(attraction_id=attraction_id).all()

    # Calculate average rating
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
        avg_rating = 0
        
    # Find nearby attractions
    nearby_attractions = Attraction.query.filter(
        Attraction.region_id == attraction.region_id,
        Attraction.id != attraction.id
    ).limit(3).all()

    return render_template('attraction_detail.html',
                           title=attraction.name,
                           attraction=attraction,
                           reviews=reviews,
                           restaurants=restaurants,
                           activities=activities,
                           avg_rating=avg_rating,
                           nearby_attractions=nearby_attractions,
                           Review=Review)  # Add Review model to template context

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user selected at least one role
        if not (form.is_guide.data or form.is_student.data or form.is_tourist.data):
            flash('Please select at least one user type.', 'danger')
            return render_template('register.html', title='Register', form=form)

        # Create new user with basic info
        user = User(
            username=form.username.data, 
            email=form.email.data,
            is_guide=form.is_guide.data,
            is_student=form.is_student.data,
            is_tourist=form.is_tourist.data,
            phone=form.phone.data,
            country=form.country.data
        )

        # Add additional information for guides and students
        if form.is_guide.data or form.is_student.data:
            user.governorate = form.governorate.data
            user.city = form.city.data
            user.education_level = form.education_level.data
            user.university = form.university.data

        # Set password and save user
        user.set_password(form.password.data)

        # Check if profile is complete
        user.profile_completed = user.is_profile_complete()

        db.session.add(user)
        db.session.commit()

        # If user is a guide, create guide profile
        if form.is_guide.data:
            guide = Guide(user_id=user.id)
            db.session.add(guide)
            db.session.commit()

        flash('Your account has been created! You can now login.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('main.index'))
        
        flash('Invalid email or password.', 'danger')

    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/profile')
@login_required
def profile():
    # If user is a guide, get guide specific info
    guide_info = None
    if current_user.is_guide:
        guide_info = Guide.query.filter_by(user_id=current_user.id).first()

        # If guide profile doesn't exist yet, create it
        if not guide_info:
            guide_info = Guide(user_id=current_user.id)
            db.session.add(guide_info)
            db.session.commit()

    # If user is a student, get language practice info
    language_practice = None
    if current_user.is_student:
        language_practice = LanguagePractice.query.filter_by(student_id=current_user.id).first()

        # If language practice profile doesn't exist yet, prepare for it
        if not language_practice:
            # We'll create it when they submit the form
            pass

    # If user is a tourist, get tour bookings
    tour_bookings = None
    if current_user.is_tourist:
        tour_bookings = TourBooking.query.filter_by(tourist_id=current_user.id).order_by(TourBooking.booking_date.desc()).all()

    # Get user's reviews
    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.date_posted.desc()).all()

    # Get chat groups if user is a guide or student
    chat_groups = []
    if current_user.is_guide:
        # Get only language practice groups for guides
        chat_groups = ChatGroup.query.filter_by(guide_id=current_user.id).all()
    elif current_user.is_student:
        # Get groups the student is a member of
        memberships = ChatGroupMember.query.filter_by(user_id=current_user.id).all()
        chat_groups = [membership.chat_group for membership in memberships]

    # Get direct message chats for guides and tourists
    direct_chats = []
    if current_user.is_guide or current_user.is_tourist:
        direct_chats = GuideTouristChat.query.filter(
            (GuideTouristChat.guide_id == current_user.id) |
            (GuideTouristChat.tourist_id == current_user.id)
        ).order_by(GuideTouristChat.created_at.desc()).all()

    # إضافة معلومات الإشعارات للسائح
    unread_count = 0
    latest_messages = []
    if current_user.is_tourist:
        unread_count = GuideTouristChat.get_unread_messages_count(current_user.id)
        latest_messages = GuideTouristChat.get_latest_messages(current_user.id)

    # Get unread messages count
    unread_messages_count = 0
    if current_user.is_guide:
        # Count unread messages for guide
        unread_messages_count = GuideTouristChat.query.filter_by(
            guide_id=current_user.id,
            is_read=False
        ).count()
    elif current_user.is_tourist:
        # Count unread messages for tourist
        unread_messages_count = GuideTouristChat.query.filter_by(
            tourist_id=current_user.id,
            is_read=False
        ).count()

    return render_template('profile.html', 
                           title='Profile',
                           guide_info=guide_info,
                           language_practice=language_practice,
                           tour_bookings=tour_bookings,
                           reviews=reviews,
                           chat_groups=chat_groups,
                           direct_chats=direct_chats,
                           unread_count=unread_count,
                           latest_messages=latest_messages,
                           unread_messages_count=unread_messages_count)

@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(original_username=current_user.username,
                      original_email=current_user.email)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.country = form.country.data
        current_user.governorate = form.governorate.data
        current_user.city = form.city.data
        current_user.education_level = form.education_level.data
        current_user.university = form.university.data
        current_user.bio = form.bio.data
        current_user.profile_pic = form.profile_pic.data

        # Update profile completion status
        current_user.profile_completed = current_user.is_profile_complete()

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.country.data = current_user.country
        form.governorate.data = current_user.governorate
        form.city.data = current_user.city
        form.education_level.data = current_user.education_level
        form.university.data = current_user.university
        form.bio.data = current_user.bio
        form.profile_pic.data = current_user.profile_pic

    # Determine which fields to show based on user type
    is_guide_or_student = current_user.is_guide or current_user.is_student

    return render_template('edit_profile.html',
                          title='Edit Profile',
                          form=form,
                          is_guide_or_student=is_guide_or_student)

@main.route('/add_review/<int:attraction_id>', methods=['GET', 'POST'])
def add_review(attraction_id): # Remove @login_required
    attraction = Attraction.query.get_or_404(attraction_id)
    form = ReviewForm()

    if form.validate_on_submit():
        # Check if user is logged in
        user_id = current_user.id if current_user.is_authenticated else None
        
        review = Review(
            title=form.title.data,
            content=form.content.data,
            rating=form.rating.data,
            user_id=user_id,
            attraction_id=attraction_id
        )
        db.session.add(review)
        db.session.commit()

        flash('Your review has been posted!', 'success')
        return redirect(url_for('main.attraction_detail', attraction_id=attraction_id))

    return render_template('add_review.html', 
                          title='Add Review',
                          form=form,
                          attraction=attraction)

@main.route('/guides')
def guides():
    # Get all guides with their user profiles
    guides = Guide.query.join(User).filter(User.is_guide==True).all()

    # Filter by language if provided
    language = request.args.get('language')
    if language:
        guides = [guide for guide in guides if language.lower() in (guide.user.languages or '').lower()]

    # Add profile info for each guide
    for guide in guides:
        guide.bio = guide.user.bio  # Use user's bio
        guide.profile_image = guide.user.profile_pic  # Use user's profile pic
        guide.languages = guide.user.languages or ''  # Use user's languages
        guide.years_experience = guide.years_experience or 0  # Use guide's experience

    return render_template('guides.html', 
                        title='Tour Guides',
                        guides=guides,
                        selected_language=language)

@main.route('/guide/<int:guide_id>')
def guide_profile(guide_id):
    # Get the guide details
    guide = Guide.query.get_or_404(guide_id)
    
    # Get guide's user profile
    user = User.query.get(guide.user_id)
    
    # Get guide's reviews
    reviews = Review.query.filter_by(user_id=guide.user_id).order_by(Review.date_posted.desc()).all()
    
    # Calculate average rating
    rating_count = len(reviews)
    average_rating = sum(review.rating for review in reviews) / rating_count if rating_count > 0 else 0
    
    return render_template('guide/profile.html',
                          title=f'Guide Profile - {user.username}',
                          guide=guide,
                          user=user,
                          reviews=reviews,
                          rating_count=rating_count,
                          average_rating=average_rating)

@main.route('/language_practice')
def language_practice():
    # Get all language practice opportunities
    opportunities = LanguagePractice.query\
        .join(User, LanguagePractice.student_id == User.id)\
        .filter(User.is_student==True).all()

    # Filter by language if provided
    language = request.args.get('language')
    if language:
        opportunities = [opp for opp in opportunities if opp.language.lower() == language.lower()]

    return render_template('language_practice.html', 
                          title='Language Practice',
                          opportunities=opportunities,
                          selected_language=language)

@main.route('/search', methods=['GET', 'POST'])
def search():
    if g.search_form.validate_on_submit() or request.args.get('q'):
        query = g.search_form.q.data or request.args.get('q', '')

        # Search in attractions
        attractions = Attraction.query.filter(
            Attraction.name.ilike(f'%{query}%') | 
            Attraction.description.ilike(f'%{query}%')
        ).all()

        # Search in restaurants
        restaurants = Restaurant.query.filter(
            Restaurant.name.ilike(f'%{query}%') | 
            Restaurant.description.ilike(f'%{query}%')
        ).all()

        # Search in activities
        activities = Activity.query.filter(
            Activity.name.ilike(f'%{query}%') | 
            Activity.description.ilike(f'%{query}%')
        ).all()

        return render_template('search_results.html',
                              title='Search Results',
                              query=query,
                              attractions=attractions,
                              restaurants=restaurants,
                              activities=activities)

    return redirect(url_for('main.index'))

# Guide Dashboard Routes
@main.route('/guide/dashboard')
@login_required
def guide_dashboard():
    if not current_user.is_guide:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get guide info
    guide = Guide.query.filter_by(user_id=current_user.id).first_or_404()

    # Get all bookings assigned to this guide
    guide_bookings = TourBooking.query.filter_by(guide_id=current_user.id)\
        .order_by(TourBooking.start_date.desc()).all()

    # Get counts
    tour_plan_count = TourPlan.query.count()
    active_booking_count = TourBooking.query.filter_by(guide_id=current_user.id, status='confirmed').count()
    
    # Get average rating for the guide
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    avg_rating = sum(review.rating for review in reviews) / len(reviews) if reviews else 0
    
    # Get recent bookings
    recent_bookings = TourBooking.query.filter_by(guide_id=current_user.id)\
        .order_by(TourBooking.booking_date.desc()).limit(5).all()
        
    # Get recent reviews
    recent_reviews = Review.query.filter_by(user_id=current_user.id)\
        .order_by(Review.date_posted.desc()).limit(3).all()

    return render_template('guide/dashboard.html',
                          title='Guide Dashboard',
                          guide=guide,
                          guide_bookings=guide_bookings,
                          tour_plan_count=tour_plan_count,
                          active_booking_count=active_booking_count,
                          avg_rating=avg_rating,
                          recent_bookings=recent_bookings,
                          recent_reviews=recent_reviews)

@main.route('/guide/chat/create', methods=['GET', 'POST'])
@login_required
def create_chat_group():
    if not current_user.is_guide:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    form = ChatGroupForm()

    if form.validate_on_submit():
        chat_group = ChatGroup(
            name=form.name.data,
            description=form.description.data,
            guide_id=current_user.id,
            language=form.language.data
        )
        db.session.add(chat_group)
        db.session.commit()

        flash('Chat group created successfully!', 'success')
        return redirect(url_for('main.guide_dashboard'))

    return render_template('guide/create_chat_group.html',
                          title='Create Chat Group',
                          form=form)

@main.route('/guide/chat/<int:chat_id>', methods=['GET', 'POST'])
@login_required
def chat_detail(chat_id):
    chat_group = ChatGroup.query.get_or_404(chat_id)

    # Check if user is the guide or a member
    is_guide = chat_group.guide_id == current_user.id
    is_member = ChatGroupMember.query.filter_by(
        user_id=current_user.id, chat_group_id=chat_id).first() is not None

    if not (is_guide or is_member):
        flash('You do not have permission to access this chat.', 'danger')
        return redirect(url_for('main.index'))

    # Form for sending messages
    form = ChatMessageForm()

    if form.validate_on_submit():
        message = ChatMessage(
            content=form.content.data,
            user_id=current_user.id,
            chat_group_id=chat_id
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('main.chat_detail', chat_id=chat_id))

    # Get all messages for this chat
    messages = ChatMessage.query.filter_by(chat_group_id=chat_id).order_by(ChatMessage.timestamp).all()

    # Get all members
    members = ChatGroupMember.query.filter_by(chat_group_id=chat_id).all()

    return render_template('chat/detail.html',
                          title=chat_group.name,
                          chat_group=chat_group,
                          form=form,
                          messages=messages,
                          members=members,
                          is_guide=is_guide)

@main.route('/guide/chat/<int:chat_id>/add_member', methods=['GET', 'POST'])
@login_required
def add_chat_member(chat_id):
    chat_group = ChatGroup.query.get_or_404(chat_id)
    
    if not current_user.is_guide:
        flash(_('فقط المرشدين يمكنهم إضافة أعضاء'), 'danger')
        return redirect(url_for('main.index'))

    try:
        # Get students who are associated with guide and not in chat
        potential_members = User.query\
            .join(LanguagePractice, User.id == LanguagePractice.student_id)\
            .outerjoin(ChatGroupMember, db.and_(
                ChatGroupMember.user_id == User.id,
                ChatGroupMember.chat_group_id == chat_id
            ))\
            .filter(
                User.is_student == True,
                LanguagePractice.guide_id == current_user.id,
                ChatGroupMember.id == None,
                LanguagePractice.language == chat_group.language
            ).all()

        if request.method == 'POST':
            try:
                # Proper CSRF validation
                validate_csrf(request.form.get('csrf_token'))
                student_id = request.form.get('student_id', type=int)
                if student_id:
                    existing = ChatGroupMember.query.filter_by(
                        chat_group_id=chat_id, 
                        user_id=student_id
                    ).first()
                    
                    if not existing:
                        new_member = ChatGroupMember(
                            chat_group_id=chat_id,
                            user_id=student_id
                        )
                        db.session.add(new_member)
                        db.session.commit()
                        flash(_('تمت إضافة الطالب بنجاح'), 'success')
                        return redirect(url_for('main.chat_detail', chat_id=chat_id))
            except ValidationError:
                flash(_('خطأ في التحقق من صحة الطلب'), 'danger')
                return redirect(url_for('main.add_chat_member', chat_id=chat_id))

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        potential_members = []
        flash(_('حدث خطأ أثناء جلب الطلاب'), 'danger')

    return render_template('guide/add_chat_member.html',
                         chat_group=chat_group,
                         potential_members=potential_members)

@main.route('/guide/tour/<int:tour_id>')
@login_required
def tour_guide_detail(tour_id):
    if not current_user.is_guide:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get booking
    booking = TourBooking.query.get_or_404(tour_id)

    # Check if guide is assigned to this tour
    if booking.guide_id != current_user.id:
        flash('You are not assigned to this tour.', 'danger')
        return redirect(url_for('main.guide_dashboard'))

    # Get tour plan and destinations
    tour_plan = booking.tour_plan
    destinations = tour_plan.destinations.order_by(TourPlanDestination.day_number).all()

    # Get current destination (first incomplete one or first one)
    current_destination = None
    for dest in destinations:
        progress = TourProgress.query.filter_by(
            booking_id=booking.id, destination_id=dest.id).first()
        if not progress or not progress.completed:
            current_destination = dest
            break

    if not current_destination and destinations:
        current_destination = destinations[0]

    # Get progress for each destination
    progress_by_dest = {}
    total_progress = 0
    progress_count = 0

    for dest in destinations:
        progress = TourProgress.query.filter_by(
            booking_id=booking.id, destination_id=dest.id).first()
        progress_by_dest[dest.id] = progress
        
        if progress and progress.progress_percentage is not None:
            total_progress += progress.progress_percentage
            progress_count += 1

    # Calculate overall progress
    overall_progress = round((total_progress / progress_count) if progress_count > 0 else 0, 2)
    
    # Check if any progress exists
    has_progress = len([p for p in progress_by_dest.values() if p is not None]) > 0

    return render_template('guide/tour_detail.html',
                          title=f'Tour: {tour_plan.title}',
                          booking=booking,
                          tour_plan=tour_plan,
                          destinations=destinations,
                          progress_by_dest=progress_by_dest,
                          current_destination=current_destination,
                          overall_progress=overall_progress,
                          has_progress=has_progress)

@main.route('/guide/booking/<int:booking_id>/confirm')
@login_required
def confirm_booking(booking_id):
    if not current_user.is_guide:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.index'))
    
    booking = TourBooking.query.get_or_404(booking_id)
    if booking.guide_id != current_user.id:
        flash('You are not assigned to this booking.', 'danger')
        return redirect(url_for('main.guide_dashboard'))
    
    booking.status = 'confirmed'
    db.session.commit()
    flash('Booking confirmed successfully!', 'success')
    return redirect(url_for('main.tour_guide_detail', tour_id=booking_id))

@main.route('/guide/booking/<int:booking_id>/reject')
@login_required
def reject_booking(booking_id):
    if not current_user.is_guide:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.index'))
    
    booking = TourBooking.query.get_or_404(booking_id)
    if booking.guide_id != current_user.id:
        flash('You are not assigned to this booking.', 'danger')
        return redirect(url_for('main.guide_dashboard'))
    
    booking.status = 'rejected'
    db.session.commit()
    flash('Booking rejected.', 'info')
    return redirect(url_for('main.tour_guide_detail', tour_id=booking_id))

@main.route('/guide/booking/<int:booking_id>/start')
@login_required
def start_tour(booking_id):
    if not current_user.is_guide:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.index'))
    
    booking = TourBooking.query.get_or_404(booking_id)
    if booking.guide_id != current_user.id:
        flash('You are not assigned to this booking.', 'danger')
        return redirect(url_for('main.guide_dashboard'))
    
    booking.status = 'in_progress'
    db.session.commit()
    flash('Tour started successfully!', 'success')
    return redirect(url_for('main.tour_guide_detail', tour_id=booking_id))

@main.route('/guide/booking/<int:booking_id>/complete')
@login_required
def complete_tour(booking_id):
    if not current_user.is_guide:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.index'))
    
    booking = TourBooking.query.get_or_404(booking_id)
    if booking.guide_id != current_user.id:
        flash('You are not assigned to this booking.', 'danger')
        return redirect(url_for('main.guide_dashboard'))
    
    booking.status = 'completed'
    db.session.commit()
    flash('Tour marked as completed!', 'success')
    return redirect(url_for('main.tour_guide_detail', tour_id=booking_id))

@main.route('/guide/booking/<int:booking_id>/cancel')
@login_required
def cancel_booking(booking_id):
    if not current_user.is_guide:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.index'))
    
    booking = TourBooking.query.get_or_404(booking_id)
    if booking.guide_id != current_user.id:
        flash('You are not assigned to this booking.', 'danger')
        return redirect(url_for('main.guide_dashboard'))
    
    booking.status = 'cancelled'
    db.session.commit()
    flash('Booking cancelled.', 'info')
    return redirect(url_for('main.tour_guide_detail', tour_id=booking_id))

@main.route('/guide/tour/<int:tour_id>/progress/<int:destination_id>', methods=['GET', 'POST'])
@login_required
def update_tour_progress(tour_id, destination_id):
    if not current_user.is_guide:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get booking and destination
    booking = TourBooking.query.get_or_404(tour_id)
    destination = TourPlanDestination.query.get_or_404(destination_id)

    # Calculate progress percentage based on total attractions
    total_destinations = booking.tour_plan.destinations.count()
    completed_destinations = TourProgress.query.filter_by(
        booking_id=booking.id,
        completed=True
    ).count()
    
    # Calculate percentage (20% for each destination)
    progress_percentage = ((completed_destinations + 1) * 100) // total_destinations

    # Get or create progress
    progress = TourProgress.query.filter_by(
        booking_id=booking.id, destination_id=destination.id).first()

    if not progress:
        progress = TourProgress(
            booking_id=booking.id,
            destination_id=destination.id,
            completed=False,
            progress_percentage=progress_percentage
        )
        db.session.add(progress)
        db.session.commit()

    # Sort previous updates by completion date
    previous_updates = TourProgress.query.filter_by(
        booking_id=booking.id
    ).order_by(TourProgress.completion_date.desc()).all()

    form = TourProgressForm()
    photo_form = TourPhotoForm()

    if form.validate_on_submit():
        try:
            progress.progress_percentage = form.progress_percentage.data
            progress.current_location = form.current_location.data
            progress.visited_attractions = form.visited_attractions.data
            progress.notes = form.notes.data
            progress.completed = True
            progress.completion_date = datetime.now()

            db.session.commit()
            flash('Progress updated successfully!', 'success')
            return redirect(url_for('main.tour_guide_detail', tour_id=tour_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating progress: {str(e)}', 'danger')
            return redirect(url_for('main.update_tour_progress', tour_id=tour_id, destination_id=destination_id))

    if not form.is_submitted():
        form.progress_percentage.data = progress.progress_percentage
        form.current_location.data = progress.current_location
        form.visited_attractions.data = progress.visited_attractions
        form.notes.data = progress.notes

    # Get photos for this progress
    photos = TourPhoto.query.filter_by(progress_id=progress.id).all() if progress else []

    return render_template('guide/update_progress.html',
                          title=f'Update Progress: {destination.attraction.name}',
                          booking=booking,
                          destination=destination,
                          progress=progress,
                          form=form,
                          photo_form=photo_form,
                          photos=photos,
                          previous_updates=previous_updates,
                          total_destinations=total_destinations,
                          completed_destinations=completed_destinations,
                          progress_per_destination=100//total_destinations)

@main.route('/guide/contact_tourist/<int:tourist_id>', methods=['GET', 'POST'])
@login_required
def contact_tourist(tourist_id):
    if not current_user.is_guide:
        flash('Only guides can access this page', 'error')
        return redirect(url_for('main.index'))
        
    tourist = User.query.get_or_404(tourist_id)
    
    # استخدام الدالة الجديدة للحصول على المحادثات
    chats = current_user.get_chats_with_user(tourist_id)
    
    form = ChatMessageForm()
    if form.validate_on_submit():
        msg = GuideTouristChat(
            guide_id=current_user.id,
            tourist_id=tourist_id,
            message=form.content.data
        )
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('main.contact_tourist', tourist_id=tourist_id))
        
    return render_template('chat/direct_chat.html', 
                         tourist=tourist,
                         chats=chats,
                         form=form)

@main.route('/contact_guide/<int:guide_id>')
@login_required 
def contact_guide(guide_id):
    if not current_user.is_tourist:
        flash('Only tourists can contact guides', 'error')
        return redirect(url_for('main.index'))
        
    guide = User.query.get_or_404(guide_id)
    if not guide.is_guide:
        flash('Invalid guide profile', 'error')
        return redirect(url_for('main.index'))
    
    # Redirect to direct chat
    return redirect(url_for('main.guide_tourist_chat', tourist_id=guide_id))

@main.route('/guide/direct_chat/<int:tourist_id>', methods=['GET', 'POST'])
@login_required
def guide_tourist_chat(tourist_id):
    if not (current_user.is_guide or current_user.is_tourist):
        flash('Only guides and tourists can access chat', 'error')
        return redirect(url_for('main.index'))
    
    # Get the other user
    other_user = User.query.get_or_404(tourist_id)
    
    if current_user.is_guide:
        guide_id = current_user.id
        chat_tourist_id = tourist_id
    else:
        guide_id = tourist_id
        chat_tourist_id = current_user.id
    
    form = ChatMessageForm()
    if form.validate_on_submit():
        # Store message in Firebase Realtime Database
        message_data = {
            'guide_id': guide_id,
            'tourist_id': chat_tourist_id,
            'message': form.content.data,
            'timestamp': datetime.utcnow().isoformat(),
            'is_read': False
        }
        
        # Send message to Firebase
        chat_ref = db_realtime.child('chats').push(message_data)
        
        # Store message locally in database
        msg = GuideTouristChat(
            guide_id=guide_id,
            tourist_id=chat_tourist_id,
            message=form.content.data,
            is_read=False
        )
        db.session.add(msg)
        db.session.commit()
        
        if request.is_json:
            return jsonify({
                'success': True,
                'message': form.content.data,
                'timestamp': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        return redirect(url_for('main.guide_tourist_chat', tourist_id=tourist_id))
    
    # Mark messages as read
    unread_messages = GuideTouristChat.query.filter_by(
        tourist_id=tourist_id if current_user.is_guide else current_user.id,
        guide_id=current_user.id if current_user.is_guide else tourist_id,
        is_read=False
    ).all()
    
    for msg in unread_messages:
        msg.is_read = True
        # تحديث حالة القراءة في Firebase
        mark_message_as_read(str(msg.id))
    db.session.commit()
    
    # Return read status for AJAX requests
    if request.is_json and request.method == 'POST':
        if 'mark_read' in request.json:
            message_id = request.json['message_id']
            message = GuideTouristChat.query.get(message_id)
            if message:
                message.is_read = True
                db.session.commit()
                return jsonify({'success': True})

    # Get chat messages between the users
    chats = GuideTouristChat.query.filter(
        ((GuideTouristChat.guide_id == current_user.id) & (GuideTouristChat.tourist_id == tourist_id)) |
        ((GuideTouristChat.guide_id == tourist_id) & (GuideTouristChat.tourist_id == current_user.id))
    ).order_by(GuideTouristChat.created_at.asc()).all()
    
    return render_template('chat/direct_chat.html', form=form, chats=chats, other_user=other_user)


@main.route('/guide/messages')
@login_required
def guide_messages():
    if not current_user.is_guide:
        flash('Only guides can access this page', 'error')
        return redirect(url_for('main.index'))
        
    # تحديث طريقة استخدام case
    chats = db.session.query(
        GuideTouristChat.tourist_id, 
        User.username,
        db.func.max(GuideTouristChat.created_at).label('last_message_time'),
        db.func.count(
            case(
                (GuideTouristChat.is_read == False, 1),
                else_=0
            )
        ).label('unread_count')
    ).join(User, User.id == GuideTouristChat.tourist_id)\
     .filter(GuideTouristChat.guide_id == current_user.id)\
     .group_by(GuideTouristChat.tourist_id, User.username)\
     .order_by(text('last_message_time DESC')).all()

    return render_template('chat/guide_messages.html', 
                         title='Messages',
                         chats=chats)

@main.route('/guide/direct_chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def direct_chat(user_id):
    if request.method == 'POST':
        if request.is_json:
            try:
                message = request.json.get('content')
                if not message:
                    return jsonify({'success': False, 'error': 'Message content is required'}), 400

                chat_message = ChatMessage(
                    sender_id=current_user.id,
                    receiver_id=user_id,
                    content=message
                )
                db.session.add(chat_message)
                db.session.commit()

                return jsonify({
                    'success': True,
                    'message_id': chat_message.id
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500

    # ... باقي الكود للطلبات GET ...

@main.route('/chat/events/<int:chat_id>')
@login_required
def chat_events(chat_id):
    def generate():
        last_id = 0
        while True:
            # Get new messages since last_id
            messages = GuideTouristChat.query.filter(
                GuideTouristChat.id > last_id,
                ((GuideTouristChat.guide_id == current_user.id) |
                 (GuideTouristChat.tourist_id == current_user.id))
            ).order_by(GuideTouristChat.created_at.asc()).all()
            
            for message in messages:
                if message.id > last_id:
                    last_id = message.id
                    data = {
                        'id': message.id,
                        'message': message.message,
                        'timestamp': message.created_at.isoformat(),
                        'sender_id': message.guide_id if message.guide_id == current_user.id else message.tourist_id
                    }
                    yield f"data: {json.dumps(data)}\n\n"
            
            time.sleep(1)  # Poll every second

    return Response(stream_with_context(generate()), 
                   mimetype='text/event-stream',
                   headers={'Cache-Control': 'no-cache',
                           'Transfer-Encoding': 'chunked'})

@main.route('/guide/language-setup', methods=['GET', 'POST'])
@login_required
def guide_language_setup():
    if not current_user.is_guide:
        flash(_('غير مصرح للوصول لهذه الصفحة'), 'error')
        return redirect(url_for('main.index'))

    form = GuideLanguageForm()
    
    if form.validate_on_submit():
        guide = Guide.query.filter_by(user_id=current_user.id).first()
        if guide:
            current_user.languages = form.languages.data
            db.session.commit()
            flash(_('تم تحديث اللغات بنجاح'), 'success')
            return redirect(url_for('main.profile'))

    if request.method == 'GET' and current_user.languages:
        form.languages.data = current_user.languages

    return render_template('guide/language_setup.html', form=form)

@main.route('/guide/setup', methods=['GET', 'POST'])
@login_required
def guide_setup():
    if not current_user.is_guide:
        flash(_('غير مصرح للوصول لهذه الصفحة'), 'error')
        return redirect(url_for('main.index'))

    form = GuideForm()
    guide = Guide.query.filter_by(user_id=current_user.id).first()
    
    if form.validate_on_submit():
        if guide:
            selected_languages = ','.join(form.languages.data) if form.languages.data else ''
            guide.specialization = form.specialization.data
            guide.years_experience = form.years_experience.data
            guide.certification = form.certification.data
            current_user.languages = selected_languages
        else:
            selected_languages = ','.join(form.languages.data) if form.languages.data else ''
            guide = Guide(
                user_id=current_user.id,
                specialization=form.specialization.data,
                years_experience=form.years_experience.data,
                certification=form.certification.data
            )
            db.session.add(guide)
            current_user.languages = selected_languages
        db.session.commit()
        flash(_('تم تحديث معلومات المرشد بنجاح'), 'success')
        return redirect(url_for('main.profile'))

    if request.method == 'GET' and guide:
        form.specialization.data = guide.specialization
        if current_user.languages:
            form.languages.data = current_user.languages.split(',')
        form.years_experience.data = guide.years_experience
        form.certification.data = guide.certification

    return render_template('guide/setup.html', form=form)

# Student Dashboard Routes
@main.route('/student/dashboard')
@login_required
def student_dashboard():
    if not current_user.is_student:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get language practice info
    language_practice = LanguagePractice.query.filter_by(student_id=current_user.id).first()

    # Get chat groups the student is a member of and materialize members
    memberships = ChatGroupMember.query.filter_by(user_id=current_user.id).all()
    chat_groups = []
    for membership in memberships:
        group = membership.chat_group
        group.member_count = ChatGroupMember.query.filter_by(chat_group_id=group.id).count()
        chat_groups.append(group)

    # Get guide if assigned
    guide = None
    if language_practice and language_practice.guide_id:
        guide_user = User.query.get(language_practice.guide_id)
        guide = Guide.query.filter_by(user_id=guide_user.id).first()

    # Get available guides for the student's language  
    available_guides = []
    if language_practice:
        guides = Guide.query.join(User).filter(User.is_guide==True).all()
        available_guides = [g for g in guides if language_practice.language.lower() in (g.user.languages or '').lower()]

    return render_template('student/dashboard.html',
                          title='Student Dashboard',
                          language_practice=language_practice, 
                          chat_groups=chat_groups,
                          guide=guide,
                          available_guides=available_guides)

@main.route('/student/select_guide/<int:guide_user_id>', methods=['GET', 'POST'])
@login_required
def select_language_guide(guide_user_id):
    """Handle guide selection for language practice"""
    if not current_user.is_student:
        flash(_('غير مصرح لك بالوصول إلى هذه الصفحة'), 'danger')
        return redirect(url_for('main.index'))

    # Get language practice info
    language_practice = LanguagePractice.query.filter_by(student_id=current_user.id).first()
    
    if not language_practice:
        flash(_('يرجى إعداد ملف ممارسة اللغة أولاً'), 'warning')
        return redirect(url_for('main.language_setup'))

    # Update the guide_id with the selected guide's user_id
    language_practice.guide_id = guide_user_id
    language_practice.selection_date = datetime.utcnow()
    db.session.commit()
    flash(_('تم اختيار المرشد بنجاح'), 'success')
    
    return redirect(url_for('main.student_dashboard'))

@main.route('/student/language_setup', methods=['GET', 'POST'])
@login_required
def language_setup():
    if not current_user.is_student:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    form = LanguagePracticeForm()

    # Check if profile already exists
    existing = LanguagePractice.query.filter_by(student_id=current_user.id).first()

    if form.validate_on_submit():
        if existing:
            # Update existing profile
            existing.language = form.language.data
            existing.proficiency_level = form.proficiency_level.data
            existing.availability = form.availability.data
            existing.interests = form.interests.data
        else:
            # Create new profile
            language_practice = LanguagePractice(
                student_id=current_user.id,
                language=form.language.data,
                proficiency_level=form.proficiency_level.data,
                availability=form.availability.data,
                interests=form.interests.data
            )
            db.session.add(language_practice)

        db.session.commit()
        flash('Language practice profile updated!', 'success')
        return redirect(url_for('main.student_dashboard'))

    if existing and not form.is_submitted():
        # Populate form with existing data
        form.language.data = existing.language
        form.proficiency_level.data = existing.proficiency_level
        form.availability.data = existing.availability
        form.interests.data = existing.interests

    return render_template('student/language_setup.html',
                          title='Language Practice Setup',
                          form=form)

@main.route('/student/find_language_guide')
@login_required
def student_find_language_guide():
    if not current_user.is_student:
        flash('Only students can access this page.', 'danger')
        return redirect(url_for('main.index'))
        
    # Get student's language practice info
    student_practice = LanguagePractice.query.filter_by(student_id=current_user.id).first()
    if not student_practice:
        flash('Please set up your language practice profile first.', 'warning')
        return redirect(url_for('main.language_setup'))
    
    # Get guides who speak the student's target language
    matching_guides = Guide.query.join(User)\
        .filter(User.is_guide==True)\
        .filter(User.languages.ilike(f'%{student_practice.language}%'))\
        .all()

    return render_template('student/find_language_guide.html',
                         guides=matching_guides,
                         student_language=student_practice.language)

# Tourist Dashboard Routes
@main.route('/tourist/dashboard')
@login_required
def tourist_dashboard():
    if not current_user.is_tourist:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get tour bookings
    bookings = TourBooking.query.filter_by(tourist_id=current_user.id).order_by(TourBooking.booking_date.desc()).all()

    # Get available tour plans
    tour_plans = TourPlan.query.all()

    return render_template('tourist/dashboard.html',
                          title='Tourist Dashboard',
                          bookings=bookings,
                          tour_plans=tour_plans)

@main.route('/tourist/tour_plans')
@login_required
def tour_plans():
    # الحصول على معرف المعلم السياحي إذا تم توفيره في عنوان URL
    attraction_id = request.args.get('attraction_id', type=int)
    
    # الحصول على جميع خطط الرحلات
    query = TourPlan.query
    
    # تصفية الخطط حسب المعلم السياحي إذا تم توفيره
    if attraction_id:
        # الحصول على الخطط التي تشمل هذا المعلم السياحي
        plans_with_attraction = []
        all_plans = query.all()
        
        for plan in all_plans:
            # التحقق مما إذا كانت الخطة تتضمن معلمًا سياحيًا محددًا
            destinations = plan.destinations.all()
            if any(dest.attraction_id == attraction_id for dest in destinations):
                plans_with_attraction.append(plan)
        
        plans = plans_with_attraction
    else:
        plans = query.all()

    return render_template('tourist/tour_plans.html',
                          title='Tour Plans',
                          plans=plans,
                          Attraction=Attraction)

@main.route('/tour_plan/<int:plan_id>')
def tour_plan_detail(plan_id):
    # Get tour plan
    plan = TourPlan.query.get_or_404(plan_id)

    # Get destinations grouped by day
    destinations_by_day = {}
    for dest in plan.destinations.order_by(TourPlanDestination.day_number).all():
        day = dest.day_number
        if day not in destinations_by_day:
            destinations_by_day[day] = []
        destinations_by_day[day].append(dest)

    # Get similar tours based on duration or price
    similar_tours = TourPlan.query.filter(
        TourPlan.id != plan_id,
        (TourPlan.duration == plan.duration) | 
        (TourPlan.price.between(plan.price * 0.8, plan.price * 1.2))
    ).limit(3).all()

    return render_template('tour_plan_detail.html',
                         title=plan.title,
                         plan=plan,
                         similar_tours=similar_tours,
                         destinations_by_day=destinations_by_day,
                         Review=Review)  # Add Review model to template context

@main.route('/tourist/book_tour/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def book_tour(plan_id):
    if not current_user.is_tourist:
        flash('You need to register as a tourist to book tours.', 'warning')
        return redirect(url_for('main.tour_plan_detail', plan_id=plan_id))

    # Get tour plan
    plan = TourPlan.query.get_or_404(plan_id)
    form = TourBookingForm()

    if form.validate_on_submit():
        try:
            start_date = datetime.strptime(form.start_date.data, '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=plan.duration)
            
            # Calculate total cost
            total_cost = plan.price * form.number_of_people.data
            
            booking = TourBooking(
                tourist_id=current_user.id,
                tour_plan_id=plan_id,
                start_date=start_date,
                end_date=end_date,
                number_of_people=form.number_of_people.data,
                notes=form.notes.data,
                status='pending',
                total_cost=total_cost,  # Save calculated total cost
                payment_status='pending'
            )
            
            db.session.add(booking)
            db.session.commit()

            flash('Tour booked successfully! Waiting for admin confirmation.', 'success')
            return redirect(url_for('main.tourist_dashboard'))
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD format.', 'danger')

    return render_template('tourist/book_tour.html',
                          title=f'Book Tour: {plan.title}',
                          plan=plan,
                          form=form)

@main.route('/tourist/tour/<int:booking_id>')
@login_required
def tour_detail(booking_id):
    # Get booking with guide relationship
    booking = TourBooking.query.join(User, TourBooking.guide_id == User.id, isouter=True)\
        .filter(TourBooking.id == booking_id).first_or_404()

    # Check if user is the tourist
    if booking.tourist_id != current_user.id:
        flash('You do not have permission to view this booking.', 'danger')
        return redirect(url_for('main.tourist_dashboard'))

    # Get tour plan and destinations
    tour_plan = booking.tour_plan
    destinations = tour_plan.destinations.order_by(TourPlanDestination.day_number).all()

    # Get progress for each destination
    progress_by_dest = {}
    photos_by_dest = {}

    for dest in destinations:
        progress = TourProgress.query.filter_by(
            booking_id=booking.id, destination_id=dest.id).first()

        if progress:
            progress_by_dest[dest.id] = progress
            photos_by_dest[dest.id] = TourPhoto.query.filter_by(progress_id=progress.id).all()
        else:
            progress_by_dest[dest.id] = None
            photos_by_dest[dest.id] = []

    return render_template('tourist/tour_detail.html',
                          title=f'Tour: {tour_plan.title}',
                          booking=booking,
                          tour_plan=tour_plan,
                          destinations=destinations,
                          progress_by_dest=progress_by_dest,
                          photos_by_dest=photos_by_dest)

@main.route('/process_payment/<int:booking_id>')
@login_required
def process_payment(booking_id):
    try:
        booking = TourBooking.query.get_or_404(booking_id)
        
        if booking.tourist_id != current_user.id:
            flash('ليس لديك صلاحية الوصول لهذا الحجز.', 'danger')
            return redirect(url_for('main.index'))
        
        if booking.payment_status == 'paid':
            flash('تم دفع هذا الحجز بالفعل.', 'info')
            return redirect(url_for('main.tour_detail', booking_id=booking_id))
        
        return render_template('tourist/payment.html',
                            booking=booking,
                            stripe_key=Config.STRIPE_PUBLIC_KEY)
                            
    except Exception as e:
        flash(f'حدث خطأ: {str(e)}', 'danger')
        return redirect(url_for('main.tour_detail', booking_id=booking_id))

@main.route('/process_stripe_payment/<int:booking_id>', methods=['POST'])
@login_required
def process_stripe_payment(booking_id):
    try:
        data = request.get_json() or {}
        csrf_token = data.get('csrf_token')
        payment_method_id = data.get('payment_method_id')
        
        # Generate return URL
        return_url = url_for('main.tourist_dashboard', _external=True)
        
        # Validate required data
        if not csrf_token or not payment_method_id:
            return jsonify({
                'success': False,
                'error': 'بيانات غير مكتملة'
            }), 400
            
        # Get booking
        booking = TourBooking.query.get_or_404(booking_id)
        
        # Create payment intent with confirm=True
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(booking.total_cost * 100),
                currency='egp',
                payment_method=payment_method_id,
                automatic_payment_methods={
                    'enabled': True,
                    'allow_redirects': 'always'
                },
                confirm=True,  # Added confirm=True to allow return_url
                return_url=return_url,
                description=f"حجز رقم {booking.id}"
            )
            
            if intent.status == 'succeeded':
                booking.payment_status = 'paid'
                booking.payment_date = datetime.utcnow()
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'redirect_url': url_for('main.tour_detail', booking_id=booking_id)
                })
            elif intent.status == 'requires_action':
                return jsonify({
                    'success': True,
                    'requires_action': True,
                    'payment_intent_client_secret': intent.client_secret,
                    'redirect_url': return_url
                })
                
        except stripe.error.CardError as e:
            return jsonify({
                'success': False,
                'error': e.user_message
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/booking/<int:booking_id>/download-itinerary')
@login_required
def download_itinerary(booking_id):
    booking = TourBooking.query.get_or_404(booking_id)
    
    # Check if user has permission to access this booking
    if not current_user.is_admin and booking.tourist_id != current_user.id and booking.guide_id != current_user.id:
        flash('You do not have permission to access this booking.', 'danger')
        return redirect(url_for('main.index'))

    # Generate itinerary content
    tour_plan = booking.tour_plan
    destinations = tour_plan.destinations.order_by(TourPlanDestination.day_number).all()
    
    # Create the itinerary text
    itinerary = f"Tour Itinerary: {tour_plan.title}\n"
    itinerary += f"Booking Date: {booking.booking_date.strftime('%Y-%m-%d')}\n"
    itinerary += f"Start Date: {booking.start_date.strftime('%Y-%m-%d')}\n"
    itinerary += f"End Date: {booking.end_date.strftime('%Y-%m-%d')}\n\n"
    
    for dest in destinations:
        itinerary += f"Day {dest.day_number}: {dest.attraction.name}\n"
        itinerary += f"{dest.description}\n\n"
    
    # Create response with file download
    response = Response(
        itinerary,
        mimetype='text/plain',
        headers={'Content-Disposition': f'attachment;filename=itinerary_{booking_id}.txt'}
    )
    
    return response

# Admin Dashboard Routes
@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Calculate counts for dashboard
    user_count = User.query.count()
    guide_count = User.query.filter_by(is_guide=True).count()
    student_count = User.query.filter_by(is_student=True).count()
    tourist_count = User.query.filter_by(is_tourist=True).count()
    
    attraction_count = Attraction.query.count()
    tour_plan_count = TourPlan.query.count()
    booking_count = TourBooking.query.count()
    
    # Get recent bookings for the table
    recent_bookings = TourBooking.query.order_by(TourBooking.booking_date.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                          title='Admin Dashboard',
                          user_count=user_count,
                          guide_count=guide_count,
                          student_count=student_count,
                          tourist_count=tourist_count,
                          attraction_count=attraction_count,
                          tour_plan_count=tour_plan_count,
                          booking_count=booking_count,
                          recent_bookings=recent_bookings)

@main.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get query parameters
    role = request.args.get('role', 'all')

    # Base query
    query = User.query

    # Filter by role
    if role == 'guide':
        query = query.filter_by(is_guide=True)
    elif role == 'student':
        query = query.filter_by(is_student=True)
    elif role == 'tourist':
        query = query.filter_by(is_tourist=True)
    elif role == 'admin':
        query = query.filter_by(is_admin=True)

    users = query.all()

    return render_template('admin/users.html',
                          title='Manage Users',
                          users=users,
                          selected_role=role)

@main.route('/admin/regions', methods=['GET', 'POST'])
@login_required
def admin_regions():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        name = request.form.get('name')
        name_ar = request.form.get('name_ar')
        description = request.form.get('description')
        description_ar = request.form.get('description_ar')

        if name:
            region = Region(
                name=name,
                name_ar=name_ar,
                description=description,
                description_ar=description_ar
            )
            db.session.add(region)
            db.session.commit()
            flash('Region added successfully!', 'success')

    regions = Region.query.all()

    return render_template('admin/regions.html',
                          title='Manage Regions',
                          regions=regions)

@main.route('/admin/attractions', methods=['GET', 'POST'])
@login_required
def admin_attractions():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        name = request.form.get('name')
        name_ar = request.form.get('name_ar')
        description = request.form.get('description')
        description_ar = request.form.get('description_ar')
        region_id = request.form.get('region_id', type=int)
        image_url = request.form.get('image_url')
        latitude = request.form.get('latitude', type=float)
        longitude = request.form.get('longitude', type=float)
        featured = 'featured' in request.form

        if name and description and region_id:
            attraction = Attraction(
                name=name,
                name_ar=name_ar,
                description=description,
                description_ar=description_ar,
                region_id=region_id,
                image_url=image_url,
                latitude=latitude,
                longitude=longitude,
                featured=featured
            )
            db.session.add(attraction)
            db.session.commit()
            flash('Attraction added successfully!', 'success')

    # Get all attractions
    attractions = Attraction.query.all()

    # Get regions for dropdown
    regions = Region.query.all()

    return render_template('admin/attractions.html',
                          title='Manage Attractions',
                          attractions=attractions,
                          regions=regions)

@main.route('/admin/tour_plans', methods=['GET', 'POST'])
@login_required
def admin_tour_plans():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    form = TourPlanForm()

    if form.validate_on_submit():
        tour_plan = TourPlan(
            title=form.title.data,
            title_ar=form.title_ar.data,
            description=form.description.data,
            description_ar=form.description_ar.data,
            duration=form.duration.data,
            price=form.price.data,
            image_url=form.image_url.data
        )
        db.session.add(tour_plan)
        db.session.commit()

        flash('Tour plan created successfully!', 'success')
        return redirect(url_for('main.admin_tour_plan_edit', plan_id=tour_plan.id))

    # Get all tour plans
    plans = TourPlan.query.all()

    return render_template('admin/tour_plans.html',
                          title='Manage Tour Plans',
                          plans=plans,
                          form=form)

@main.route('/admin/tour_plans/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def admin_tour_plan_edit(plan_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get tour plan
    plan = TourPlan.query.get_or_404(plan_id)

    # Form for editing plan details
    form = TourPlanForm()

    # Form for adding destinations
    destination_form = TourPlanDestinationForm()

    # Populate attractions dropdown
    destination_form.attraction_id.choices = [(a.id, a.name) for a in Attraction.query.all()]

    if form.validate_on_submit():
        plan.title = form.title.data
        plan.title_ar = form.title_ar.data
        plan.description = form.description.data
        plan.description_ar = form.description_ar.data
        plan.duration = form.duration.data
        plan.price = form.price.data
        plan.image_url = form.image_url.data

        db.session.commit()
        flash('Tour plan updated successfully!', 'success')
        return redirect(url_for('main.admin_tour_plan_edit', plan_id=plan.id))

    if destination_form.validate_on_submit():
        destination = TourPlanDestination(
            tour_plan_id=plan.id,
            attraction_id=destination_form.attraction_id.data,
            day_number=destination_form.day_number.data,
            description=destination_form.description.data,
            description_ar=destination_form.description_ar.data
        )

        db.session.add(destination)
        db.session.commit()

        flash('Destination added successfully!', 'success')
        return redirect(url_for('main.admin_tour_plan_edit', plan_id=plan.id))

    # Get destinations
    destinations = plan.destinations.order_by(TourPlanDestination.day_number).all()

    if not form.is_submitted():
        # Populate form with existing data
        form.title.data = plan.title
        form.title_ar.data = plan.title_ar
        form.description.data = plan.description
        form.description_ar.data = plan.description_ar
        form.duration.data = plan.duration
        form.price.data = plan.price
        form.image_url.data = plan.image_url

    return render_template('admin/tour_plan_edit.html',
                          title=f'Edit Tour Plan: {plan.title}',
                          plan=plan,
                          form=form,
                          destination_form=destination_form,
                          destinations=destinations)

@main.route('/admin/bookings')
@login_required
def admin_bookings():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get query parameters
    status = request.args.get('status', 'all')

    # Base query
    query = TourBooking.query

    # Filter by status
    if status != 'all':
        query = query.filter_by(status=status)

    # Get bookings
    bookings = query.order_by(TourBooking.booking_date.desc()).all()

    return render_template('admin/bookings.html',
                          title='Manage Bookings',
                          bookings=bookings,
                          selected_status=status)

@main.route('/admin/booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def admin_booking_detail(booking_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get booking
    booking = TourBooking.query.get_or_404(booking_id)

    # Form for assigning guide
    form = AssignGuideForm()

    # Populate guides dropdown
    form.guide_id.choices = [(g.user_id, g.user.username) for g in Guide.query.join(User).all()]

    if form.validate_on_submit():
        booking.guide_id = form.guide_id.data
        booking.status = 'confirmed'
        db.session.commit()

        flash('Guide assigned and booking confirmed!', 'success')
        return redirect(url_for('main.admin_bookings'))

    if request.method == 'POST' and 'status' in request.form:
        booking.status = request.form['status']
        db.session.commit()

        flash('Booking status updated!', 'success')
        return redirect(url_for('main.admin_booking_detail', booking_id=booking.id))

    # If form not submitted and guide not assigned, set form defaults
    if not form.is_submitted() and booking.guide_id:
        form.guide_id.data = booking.guide_id

    return render_template('admin/booking_detail.html',
                          title=f'Booking: {booking.tour_plan.title}',
                          booking=booking,
                          form=form)

@main.route('/admin/chat_groups')
@login_required
def admin_chat_groups():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get all chat groups
    chat_groups = ChatGroup.query.all()

    return render_template('admin/chat_groups.html',
                          title='Manage Chat Groups',
                          chat_groups=chat_groups)

# API routes for JavaScript functionality
@main.route('/api/attractions', methods=['GET'])
def api_attractions():
    attractions = Attraction.query.all()
    result = []

    for attraction in attractions:
        result.append({
            'id': attraction.id,
            'name': attraction.name,
            'latitude': attraction.latitude,
            'longitude': attraction.longitude
        })

    return jsonify(result)

# Error handlers
@main.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500