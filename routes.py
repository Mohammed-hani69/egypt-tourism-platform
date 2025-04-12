from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from extensions import db, babel
from models import (User, Attraction, Region, Review, Restaurant, Activity, Guide, LanguagePractice,
                    ChatGroup, ChatGroupMember, ChatMessage, TourPlan, TourPlanDestination, 
                    TourBooking, TourProgress, TourPhoto)
from forms import (RegistrationForm, LoginForm, ReviewForm, GuideForm, LanguagePracticeForm, SearchForm,
                   ChatGroupForm, ChatMessageForm, SelectGuideForm, TourPlanForm, TourPlanDestinationForm, 
                   TourBookingForm, AssignGuideForm, TourProgressForm, TourPhotoForm, ProfileForm)
from datetime import datetime, date, timedelta
import os

# Create blueprint
main = Blueprint('main', __name__)

# Set up locale selector
def get_locale():
    # Try to get the language from the session
    if 'language' in session:
        return session['language']
    # Default to English
    return 'en'

@main.before_app_request
def before_request():
    g.locale = str(get_locale())
    g.search_form = SearchForm()

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

    # Get reviews for this attraction
    reviews = Review.query.filter_by(attraction_id=attraction_id).order_by(Review.date_posted.desc()).all()

    # Get nearby restaurants
    restaurants = Restaurant.query.filter_by(attraction_id=attraction_id).all()

    # Get available activities
    activities = Activity.query.filter_by(attraction_id=attraction_id).all()

    # Calculate average rating
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
        avg_rating = 0

    return render_template('attraction_detail.html',
                           title=attraction.name,
                           attraction=attraction,
                           reviews=reviews,
                           restaurants=restaurants,
                           activities=activities,
                           avg_rating=avg_rating)

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
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

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
        chat_groups = ChatGroup.query.filter_by(guide_id=current_user.id).all()
    elif current_user.is_student:
        # Get groups the student is a member of
        memberships = ChatGroupMember.query.filter_by(user_id=current_user.id).all()
        chat_groups = [membership.chat_group for membership in memberships]

    return render_template('profile.html', 
                           title='Profile',
                           guide_info=guide_info,
                           language_practice=language_practice,
                           tour_bookings=tour_bookings,
                           reviews=reviews,
                           chat_groups=chat_groups)

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
@login_required
def add_review(attraction_id):
    attraction = Attraction.query.get_or_404(attraction_id)
    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            title=form.title.data,
            content=form.content.data,
            rating=form.rating.data,
            user_id=current_user.id,
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
    # Get all guides
    guides = Guide.query.join(User).filter(User.is_guide==True).all()

    # Filter by language if provided
    language = request.args.get('language')
    if language:
        guides = [guide for guide in guides if language.lower() in (guide.user.languages or '').lower()]

    return render_template('guides.html', 
                          title='Tour Guides',
                          guides=guides,
                          selected_language=language)

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

    # Get students assigned to this guide
    students = LanguagePractice.query.filter_by(guide_id=current_user.id).all()

    # Get chat groups created by this guide
    chat_groups = ChatGroup.query.filter_by(guide_id=current_user.id).all()

    # Get tours assigned to this guide
    guided_tours = TourBooking.query.filter_by(guide_id=current_user.id).all()

    return render_template('guide/dashboard.html',
                          title='Guide Dashboard',
                          guide=guide,
                          students=students,
                          chat_groups=chat_groups,
                          guided_tours=guided_tours)

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

    # Only the guide can add members
    if chat_group.guide_id != current_user.id:
        flash('You do not have permission to add members to this chat.', 'danger')
        return redirect(url_for('main.chat_detail', chat_id=chat_id))

    # Get students who are learning the language of this chat
    potential_members = LanguagePractice.query\
        .join(User, LanguagePractice.student_id == User.id)\
        .filter(LanguagePractice.language == chat_group.language).all()

    # Filter out students who are already members
    existing_member_ids = [m.user_id for m in ChatGroupMember.query.filter_by(chat_group_id=chat_id).all()]
    potential_members = [p for p in potential_members if p.student_id not in existing_member_ids]

    if request.method == 'POST':
        student_id = request.form.get('student_id', type=int)

        if student_id:
            member = ChatGroupMember(
                user_id=student_id,
                chat_group_id=chat_id
            )
            db.session.add(member)
            db.session.commit()

            flash('Member added successfully!', 'success')
            return redirect(url_for('main.chat_detail', chat_id=chat_id))

    return render_template('guide/add_chat_member.html',
                          title='Add Member to Chat',
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

    # Get progress for each destination
    progress_by_dest = {}
    for dest in destinations:
        progress = TourProgress.query.filter_by(
            booking_id=booking.id, destination_id=dest.id).first()
        progress_by_dest[dest.id] = progress

    return render_template('guide/tour_detail.html',
                          title=f'Tour: {tour_plan.title}',
                          booking=booking,
                          tour_plan=tour_plan,
                          destinations=destinations,
                          progress_by_dest=progress_by_dest)

@main.route('/guide/tour/<int:tour_id>/progress/<int:destination_id>', methods=['GET', 'POST'])
@login_required
def update_tour_progress(tour_id, destination_id):
    if not current_user.is_guide:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get booking and destination
    booking = TourBooking.query.get_or_404(tour_id)
    destination = TourPlanDestination.query.get_or_404(destination_id)

    # Check if guide is assigned to this tour
    if booking.guide_id != current_user.id:
        flash('You are not assigned to this tour.', 'danger')
        return redirect(url_for('main.guide_dashboard'))

    # Get or create progress
    progress = TourProgress.query.filter_by(
        booking_id=booking.id, destination_id=destination.id).first()

    if not progress:
        progress = TourProgress(
            booking_id=booking.id,
            destination_id=destination.id,
            completed=False
        )
        db.session.add(progress)
        db.session.commit()

    form = TourProgressForm()
    photo_form = TourPhotoForm()

    if form.validate_on_submit():
        progress.notes = form.notes.data
        progress.completed = True
        progress.completion_date = datetime.now()
        db.session.commit()

        flash('Progress updated successfully!', 'success')
        return redirect(url_for('main.tour_guide_detail', tour_id=tour_id))

    if photo_form.validate_on_submit():
        photo = TourPhoto(
            progress_id=progress.id,
            image_url=photo_form.image_url.data,
            caption=photo_form.caption.data
        )
        db.session.add(photo)
        db.session.commit()

        flash('Photo added successfully!', 'success')
        return redirect(url_for('main.update_tour_progress', tour_id=tour_id, destination_id=destination_id))

    # Get photos
    photos = TourPhoto.query.filter_by(progress_id=progress.id).all()

    if not form.is_submitted():
        form.notes.data = progress.notes

    return render_template('guide/update_progress.html',
                          title=f'Update Progress: {destination.attraction.name}',
                          booking=booking,
                          destination=destination,
                          progress=progress,
                          form=form,
                          photo_form=photo_form,
                          photos=photos)

# Student Dashboard Routes
@main.route('/student/dashboard')
@login_required
def student_dashboard():
    if not current_user.is_student:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get language practice info
    language_practice = LanguagePractice.query.filter_by(student_id=current_user.id).first()

    # Get chat groups the student is a member of
    memberships = ChatGroupMember.query.filter_by(user_id=current_user.id).all()
    chat_groups = [membership.chat_group for membership in memberships]

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

@main.route('/student/select_guide/<int:guide_id>')
@login_required
def select_guide(guide_id):
    if not current_user.is_student:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get language practice info
    language_practice = LanguagePractice.query.filter_by(student_id=current_user.id).first()

    if not language_practice:
        flash('Please set up your language practice profile first.', 'warning')
        return redirect(url_for('main.student_dashboard'))

    # Set guide
    language_practice.guide_id = guide_id
    db.session.commit()

    flash('Guide selected successfully!', 'success')
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
    # Get all tour plans
    plans = TourPlan.query.all()

    return render_template('tourist/tour_plans.html',
                          title='Tour Plans',
                          plans=plans)

@main.route('/tour_plan/<int:plan_id>')
@main.route('/tourist/tour_plan/<int:plan_id>')
def tour_plan_detail(plan_id):
    plan = TourPlan.query.get_or_404(plan_id)

    # الحصول على الخطط السياحية المشابهة (نفس المدة أو السعر المشابه)
    similar_tours = TourPlan.query.filter(
        TourPlan.id != plan_id,
        (TourPlan.duration == plan.duration) | 
        (TourPlan.price.between(plan.price * 0.8, plan.price * 1.2))
    ).limit(3).all()

    return render_template('tour_plan_detail.html',
                          title=plan.title,
                          plan=plan,
                          similar_tours=similar_tours)
def tour_plan_detail(plan_id):
    # Get tour plan
    plan = TourPlan.query.get_or_404(plan_id)

    # Get destinations grouped by day
    destinations_by_day = {}
    for dest in plan.destinations.order_by(TourPlanDestination.day_number).all():
        if dest.day_number not in destinations_by_day:
            destinations_by_day[dest.day_number] = []

        destinations_by_day[dest.day_number].append(dest)

    return render_template('tourist/tour_plan_detail.html',
                          title=plan.title,
                          plan=plan,
                          destinations_by_day=destinations_by_day)

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
        # Convert string date to datetime object
        try:
            start_date = datetime.strptime(form.start_date.data, '%Y-%m-%d').date()
            # Calculate end date based on tour duration
            end_date = start_date + timedelta(days=plan.duration)

            booking = TourBooking(
                tourist_id=current_user.id,
                tour_plan_id=plan_id,
                start_date=start_date,
                end_date=end_date,
                number_of_people=form.number_of_people.data,
                notes=form.notes.data,
                status='pending'
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
    # Get booking
    booking = TourBooking.query.get_or_404(booking_id)

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

# Admin Dashboard Routes
@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Get counts for dashboard
    users_count = User.query.count()
    guides_count = User.query.filter_by(is_guide=True).count()
    students_count = User.query.filter_by(is_student=True).count()
    tourists_count = User.query.filter_by(is_tourist=True).count()

    attractions_count = Attraction.query.count()
    regions_count = Region.query.count()

    bookings_count = TourBooking.query.count()
    pending_bookings = TourBooking.query.filter_by(status='pending').count()

    chat_groups_count = ChatGroup.query.count()

    return render_template('admin/dashboard.html',
                          title='Admin Dashboard',
                          users_count=users_count,
                          guides_count=guides_count,
                          students_count=students_count,
                          tourists_count=tourists_count,
                          attractions_count=attractions_count,
                          regions_count=regions_count,
                          bookings_count=bookings_count,
                          pending_bookings=pending_bookings,
                          chat_groups_count=chat_groups_count)

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