from flask import render_template, redirect, url_for, flash, request, jsonify, session, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from flask_babel import get_locale
from app import app, db, babel
from models import User, Attraction, Region, Review, Restaurant, Activity, Guide, LanguagePractice
from forms import RegistrationForm, LoginForm, ReviewForm, GuideForm, LanguagePracticeForm, SearchForm
import os


# Set up locale selector
def get_locale():
    # Try to get the language from the session
    if 'language' in session:
        return session['language']
    # Default to English
    return 'en'

babel.init_app(app, locale_selector=get_locale)


@app.before_request
def before_request():
    g.locale = str(get_locale())
    g.search_form = SearchForm()


@app.route('/set_language/<language>')
def set_language(language):
    session['language'] = language
    return redirect(request.referrer or url_for('index'))


@app.route('/')
def index():
    # Get featured attractions
    featured_attractions = Attraction.query.filter_by(featured=True).limit(4).all()
    
    # Get all regions for the navigation
    regions = Region.query.all()
    
    return render_template('index.html', 
                           title='Home',
                           featured_attractions=featured_attractions,
                           regions=regions)


@app.route('/attractions')
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


@app.route('/attraction/<int:attraction_id>')
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    email=form.email.data,
                    is_guide=form.is_guide.data,
                    is_student=form.is_student.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    # If user is a guide, get guide specific info
    guide_info = None
    if current_user.is_guide:
        guide_info = Guide.query.filter_by(user_id=current_user.id).first()
    
    # If user is a student, get language practice info
    language_practice = None
    if current_user.is_student:
        language_practice = LanguagePractice.query.filter_by(student_id=current_user.id).first()
    
    # Get user's reviews
    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.date_posted.desc()).all()
    
    return render_template('profile.html', 
                           title='Profile',
                           guide_info=guide_info,
                           language_practice=language_practice,
                           reviews=reviews)


@app.route('/add_review/<int:attraction_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('attraction_detail', attraction_id=attraction_id))
    
    return render_template('add_review.html', 
                          title='Add Review',
                          form=form,
                          attraction=attraction)


@app.route('/guides')
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


@app.route('/language_practice')
def language_practice():
    # Get all language practice opportunities
    opportunities = LanguagePractice.query.join(User).filter(User.is_student==True).all()
    
    # Filter by language if provided
    language = request.args.get('language')
    if language:
        opportunities = [opp for opp in opportunities if opp.language.lower() == language.lower()]
    
    return render_template('language_practice.html', 
                          title='Language Practice',
                          opportunities=opportunities,
                          selected_language=language)


@app.route('/search', methods=['GET', 'POST'])
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
    
    return redirect(url_for('index'))


# API routes for JavaScript functionality
@app.route('/api/attractions', methods=['GET'])
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
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
