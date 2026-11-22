import sys
import os

# Ensure backend directory is in python search path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import py_loader
import re
from datetime import datetime, timezone
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, jsonify, g, abort
)
from config import Config
from models import (
    db, User, Project, CommunityPost, PostComment,
    SavedCalculation, FeedbackMessage, EnergyTip, EducationalArticle
)

TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'static')

if not os.path.isdir(TEMPLATE_DIR):
    TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
if not os.path.isdir(STATIC_DIR):
    STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')

def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR
    )
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Automatically create tables if not existing on first request/startup
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"[Warning] db.create_all() error: {e}")

    # Authentication helper decorator
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in or register to access this feature.', 'warning')
                return redirect(url_for('login', next=request.url))
            return f(*args, **kwargs)
        return decorated_function

    # Context processor to inject global variables into templates
    @app.context_processor
    def inject_globals():
        current_user = None
        if 'user_id' in session:
            current_user = db.session.get(User, session['user_id'])
        
        # Fast cached aggregate counts for nav badges or footers
        try:
            total_members = User.query.count()
            total_projects = Project.query.count()
        except Exception:
            total_members = 0
            total_projects = 0

        return {
            'current_user': current_user,
            'current_year': datetime.now(timezone.utc).year,
            'global_total_members': total_members,
            'global_total_projects': total_projects
        }

    # =========================================================================
    # 1. HOME PAGE
    # =========================================================================
    @app.route('/')
    def index():
        try:
            featured_projects = Project.query.order_by(Project.annual_generation.desc()).limit(3).all()
            latest_posts = CommunityPost.query.order_by(CommunityPost.created_at.desc()).limit(3).all()
            total_members = User.query.count()
            total_projects = Project.query.count()
            
            # Aggregate environmental metrics
            projects = Project.query.all()
            total_generation = sum(p.annual_generation for p in projects)
            total_co2 = sum(p.co2_saved_annual for p in projects)
            total_participants = sum(p.participants_count for p in projects)
        except Exception:
            featured_projects = []
            latest_posts = []
            total_members = 150
            total_projects = 5
            total_generation = 8170.0
            total_co2 = 5723.0
            total_participants = 707

        return render_template(
            'index.html',
            featured_projects=featured_projects,
            latest_posts=latest_posts,
            total_members=total_members,
            total_projects=total_projects,
            total_generation=round(total_generation, 1),
            total_co2=round(total_co2, 1),
            total_participants=total_participants
        )

    # =========================================================================
    # 2. RENEWABLE ENERGY AWARENESS
    # =========================================================================
    @app.route('/awareness')
    def awareness():
        selected_category = request.args.get('category', 'All')
        
        if selected_category and selected_category != 'All':
            articles = EducationalArticle.query.filter_by(category=selected_category).order_by(EducationalArticle.id.asc()).all()
            tips = EnergyTip.query.filter_by(category=selected_category).all()
        else:
            articles = EducationalArticle.query.order_by(EducationalArticle.id.asc()).all()
            tips = EnergyTip.query.order_by(EnergyTip.potential_savings_kwh.desc()).all()

        return render_template(
            'awareness.html',
            articles=articles,
            tips=tips,
            selected_category=selected_category
        )

    @app.route('/awareness/article/<slug>')
    def article_detail(slug):
        article = EducationalArticle.query.filter_by(slug=slug).first_or_404()
        related_articles = EducationalArticle.query.filter(EducationalArticle.id != article.id).limit(3).all()
        return render_template('article_detail.html', article=article, related_articles=related_articles)

    # =========================================================================
    # 3. ENERGY SAVINGS CALCULATOR
    # =========================================================================
    @app.route('/calculator')
    def calculator():
        user_calculations = []
        if 'user_id' in session:
            user_calculations = SavedCalculation.query.filter_by(user_id=session['user_id']).order_by(SavedCalculation.created_at.desc()).limit(5).all()
        return render_template('calculator.html', user_calculations=user_calculations)

    @app.route('/api/calculate-savings', methods=['POST'])
    def calculate_savings_api():
        data = request.get_json() or {}
        try:
            monthly_bill = float(data.get('monthly_bill', 150.0))
            tariff_rate = float(data.get('tariff_rate', 0.16))  # $ or local currency per kWh
            sunlight_hours = float(data.get('sunlight_hours', 5.0))  # avg daily peak sun hours
            roof_area = float(data.get('roof_area', 500.0))  # sq. ft.
            offset_percentage = float(data.get('offset_percentage', 100.0)) / 100.0

            # Guard rails
            monthly_bill = max(10.0, monthly_bill)
            tariff_rate = max(0.04, min(1.0, tariff_rate))
            sunlight_hours = max(2.5, min(8.0, sunlight_hours))
            offset_percentage = max(0.2, min(1.5, offset_percentage))

            # Monthly consumption in kWh
            monthly_kwh = monthly_bill / tariff_rate
            annual_kwh = monthly_kwh * 12

            # Target solar kWh needed annually
            target_annual_solar_kwh = annual_kwh * offset_percentage

            # Solar System capacity formula:
            # Capacity (kW) = Annual kWh / (Sunlight hours * 365 * System Performance Ratio 0.78)
            system_performance_ratio = 0.78
            recommended_kw = target_annual_solar_kwh / (sunlight_hours * 365 * system_performance_ratio)
            recommended_kw = round(recommended_kw, 2)

            # Check roof feasibility: typically 1 kW needs ~70-80 sq ft of roof space
            required_roof_area = round(recommended_kw * 75, 1)
            roof_adequate = (roof_area >= required_roof_area)

            # Solar generation
            annual_solar_generation = round(recommended_kw * sunlight_hours * 365 * system_performance_ratio, 1)
            monthly_solar_generation = round(annual_solar_generation / 12, 1)

            # Bill savings
            monthly_savings = min(monthly_bill, round(monthly_solar_generation * tariff_rate, 2))
            annual_savings = round(monthly_savings * 12, 2)

            # Estimated capital cost (~$2.80 per watt installed before incentives, minus 30% federal/state tax credit)
            gross_cost = recommended_kw * 1000 * 2.80
            net_system_cost = gross_cost * 0.70  # after 30% incentive
            payback_years = round(net_system_cost / annual_savings, 1) if annual_savings > 0 else 0

            # Environmental benefits (US EPA factor: ~0.709 kg CO2/kWh displaced)
            annual_co2_saved_tons = round(annual_solar_generation * 0.000709, 2)
            trees_equivalent = int(round(annual_co2_saved_tons * 1000 / 21.77))
            car_miles_avoided = int(round(annual_co2_saved_tons * 2480))

            # 25-Year cumulative savings projection (assuming 3% annual utility rate escalation)
            cumulative_savings_25yr = []
            cumulative_cost_without_solar = []
            curr_savings_accum = 0.0
            curr_nosolar_accum = 0.0
            rate_factor = 1.0

            for yr in range(1, 26):
                rate_factor *= 1.03
                curr_nosolar_accum += (annual_kwh * tariff_rate * rate_factor)
                curr_savings_accum += (annual_savings * rate_factor)
                if yr in [1, 5, 10, 15, 20, 25]:
                    cumulative_savings_25yr.append({
                        'year': yr,
                        'cumulative_savings': round(curr_savings_accum, 0),
                        'cost_without_solar': round(curr_nosolar_accum, 0)
                    })

            return jsonify({
                'success': True,
                'monthly_bill': round(monthly_bill, 2),
                'monthly_kwh': round(monthly_kwh, 1),
                'annual_kwh': round(annual_kwh, 1),
                'recommended_kw': recommended_kw,
                'panels_count': int(round(recommended_kw * 1000 / 400)), # 400W panels
                'required_roof_area': required_roof_area,
                'roof_adequate': roof_adequate,
                'monthly_solar_generation': monthly_solar_generation,
                'annual_solar_generation': annual_solar_generation,
                'monthly_savings': monthly_savings,
                'annual_savings': annual_savings,
                'net_system_cost': round(net_system_cost, 0),
                'payback_years': payback_years,
                'annual_co2_saved_tons': annual_co2_saved_tons,
                'trees_equivalent': trees_equivalent,
                'car_miles_avoided': car_miles_avoided,
                'projection_25yr': cumulative_savings_25yr
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    @app.route('/api/save-calculation', methods=['POST'])
    @login_required
    def save_calculation_api():
        data = request.get_json() or {}
        try:
            calc = SavedCalculation(
                user_id=session.get('user_id'),
                monthly_bill=float(data.get('monthly_bill', 0)),
                monthly_kwh=float(data.get('monthly_kwh', 0)),
                tariff_rate=float(data.get('tariff_rate', 0.16)),
                roof_area_sqft=float(data.get('roof_area', 500)),
                sunlight_hours=float(data.get('sunlight_hours', 5)),
                recommended_kw=float(data.get('recommended_kw', 5)),
                monthly_savings=float(data.get('monthly_savings', 0)),
                annual_savings=float(data.get('annual_savings', 0)),
                co2_reduction_tons=float(data.get('annual_co2_saved_tons', 0)),
                trees_equivalent=int(data.get('trees_equivalent', 0)),
                payback_years=float(data.get('payback_years', 0))
            )
            db.session.add(calc)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Calculation successfully saved to your profile!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 400

    # =========================================================================
    # 4. COMMUNITY MANAGEMENT & FORUM
    # =========================================================================
    @app.route('/community')
    def community():
        category = request.args.get('category', 'All')
        query = CommunityPost.query
        if category and category != 'All':
            query = query.filter_by(category=category)
        
        posts = query.order_by(CommunityPost.created_at.desc()).all()
        categories = ['All', 'Solar Experience', 'Wind & DIY', 'Energy Tips', 'Policy & Subsidy', 'General Discussion']
        return render_template('community.html', posts=posts, categories=categories, selected_category=category)

    @app.route('/community/post', methods=['POST'])
    @login_required
    def create_post():
        title = request.form.get('title', '').strip()
        category = request.form.get('category', 'General Discussion').strip()
        content = request.form.get('content', '').strip()

        if not title or len(title) < 5:
            flash('Post title must be at least 5 characters long.', 'danger')
            return redirect(url_for('community'))

        if not content or len(content) < 15:
            flash('Please provide more details in your post (minimum 15 characters).', 'danger')
            return redirect(url_for('community'))

        post = CommunityPost(
            user_id=session['user_id'],
            title=title,
            category=category,
            content=content,
            upvotes=0
        )
        db.session.add(post)
        db.session.commit()
        flash('Your community experience/story has been posted successfully!', 'success')
        return redirect(url_for('community'))

    @app.route('/community/post/<int:post_id>/comment', methods=['POST'])
    @login_required
    def add_comment(post_id):
        post = db.get_or_404(CommunityPost, post_id)
        content = request.form.get('content', '').strip()

        if not content:
            flash('Comment cannot be empty.', 'danger')
            return redirect(url_for('community'))

        comment = PostComment(
            post_id=post.id,
            user_id=session['user_id'],
            content=content
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
        return redirect(url_for('community'))

    @app.route('/api/post/<int:post_id>/upvote', methods=['POST'])
    @login_required
    def upvote_post_api(post_id):
        post = db.get_or_404(CommunityPost, post_id)
        post.upvotes += 1
        db.session.commit()
        return jsonify({'success': True, 'upvotes': post.upvotes})

    # =========================================================================
    # 5. RENEWABLE ENERGY PROJECTS
    # =========================================================================
    @app.route('/projects')
    def projects():
        category = request.args.get('category', 'All')
        status = request.args.get('status', 'All')

        query = Project.query
        if category and category != 'All':
            query = query.filter_by(category=category)
        if status and status != 'All':
            query = query.filter_by(status=status)

        all_projects = query.order_by(Project.created_at.desc()).all()
        return render_template(
            'projects.html',
            projects=all_projects,
            selected_category=category,
            selected_status=status
        )

    @app.route('/projects/<int:project_id>')
    def project_detail(project_id):
        project = db.get_or_404(Project, project_id)
        other_projects = Project.query.filter(Project.id != project.id).limit(3).all()
        return render_template('project_detail.html', project=project, other_projects=other_projects)

    @app.route('/projects/propose', methods=['POST'])
    @login_required
    def propose_project():
        title = request.form.get('title', '').strip()
        category = request.form.get('category', 'Solar').strip()
        location = request.form.get('location', '').strip()
        capacity = request.form.get('capacity', '').strip()
        budget = request.form.get('budget', 0)
        description = request.form.get('description', '').strip()
        installation_guide = request.form.get('installation_guide', '').strip()

        if not title or not location or not capacity or not description:
            flash('Please complete all required fields to propose a community project.', 'danger')
            return redirect(url_for('projects'))

        try:
            budget_val = float(budget) if budget else 0.0
        except ValueError:
            budget_val = 0.0

        # Create slug
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
        existing = Project.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{int(datetime.now(timezone.utc).timestamp())}"

        try:
            cap_num = float(re.findall(r'\d+(?:\.\d+)?', capacity)[0])
            if 'mw' in capacity.lower():
                cap_num *= 1000
        except Exception:
            cap_num = 100.0

        annual_gen = round(cap_num * 1.5, 1)
        annual_co2 = round(annual_gen * 0.7, 1)

        project = Project(
            title=title,
            slug=slug,
            category=category,
            description=description,
            location=location,
            capacity=capacity,
            annual_generation=annual_gen,
            co2_saved_annual=annual_co2,
            participants_count=1,
            status='Planning',
            budget=budget_val,
            installation_guide=installation_guide or "Under community committee formulation.",
            image_url=f"{category.lower()}_project.svg",
            created_by_id=session['user_id']
        )
        db.session.add(project)
        db.session.commit()
        flash('Your community renewable energy project proposal has been submitted for review!', 'success')
        return redirect(url_for('projects'))

    # =========================================================================
    # 6. DASHBOARD
    # =========================================================================
    @app.route('/dashboard')
    def dashboard():
        total_users = User.query.count()
        all_projects = Project.query.all()
        total_projects_count = len(all_projects)
        active_projects_count = sum(1 for p in all_projects if p.status == 'Active')

        total_annual_generation = sum(p.annual_generation for p in all_projects)
        total_annual_co2 = sum(p.co2_saved_annual for p in all_projects)
        total_participants = sum(p.participants_count for p in all_projects)

        estimated_community_savings = round(total_annual_generation * 160.0, 2)

        categories = ['Solar', 'Wind', 'Hydro', 'Biomass']
        category_generation = {}
        category_counts = {}
        for cat in categories:
            projs = [p for p in all_projects if p.category == cat]
            category_generation[cat] = round(sum(p.annual_generation for p in projs), 1)
            category_counts[cat] = len(projs)

        recent_posts = CommunityPost.query.order_by(CommunityPost.created_at.desc()).limit(5).all()
        recent_feedback = FeedbackMessage.query.order_by(FeedbackMessage.created_at.desc()).limit(5).all()

        user_calculations = []
        user_posts = []
        if 'user_id' in session:
            user_calculations = SavedCalculation.query.filter_by(user_id=session['user_id']).order_by(SavedCalculation.created_at.desc()).all()
            user_posts = CommunityPost.query.filter_by(user_id=session['user_id']).all()

        return render_template(
            'dashboard.html',
            total_users=total_users,
            total_projects=total_projects_count,
            active_projects=active_projects_count,
            total_generation=round(total_annual_generation, 1),
            total_co2=round(total_annual_co2, 1),
            total_participants=total_participants,
            estimated_community_savings=estimated_community_savings,
            category_generation=category_generation,
            category_counts=category_counts,
            recent_posts=recent_posts,
            recent_feedback=recent_feedback,
            user_calculations=user_calculations,
            user_posts=user_posts
        )

    @app.route('/api/dashboard/stats')
    def dashboard_stats_api():
        all_projects = Project.query.all()
        categories = ['Solar', 'Wind', 'Hydro', 'Biomass']
        generation_by_source = [round(sum(p.annual_generation for p in all_projects if p.category == cat), 1) for cat in categories]
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_trend = [420, 460, 580, 690, 810, 920, 960, 910, 780, 640, 510, 440]
        monthly_savings = [round(m * 160 / 1000, 1) for m in monthly_trend]

        return jsonify({
            'sources': categories,
            'generation_by_source': generation_by_source,
            'months': months,
            'monthly_generation_mwh': monthly_trend,
            'monthly_savings_k': monthly_savings
        })

    # =========================================================================
    # 7. CONTACT & FEEDBACK
    # =========================================================================
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip()
            category = request.form.get('category', 'General Feedback').strip()
            message = request.form.get('message', '').strip()

            if not name or len(name) < 2:
                flash('Please provide your full name.', 'danger')
                return render_template('contact.html', form_data=request.form)

            email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not email or not re.match(email_regex, email):
                flash('Please provide a valid email address.', 'danger')
                return render_template('contact.html', form_data=request.form)

            if not subject or len(subject) < 3:
                flash('Please provide a meaningful subject.', 'danger')
                return render_template('contact.html', form_data=request.form)

            if not message or len(message) < 10:
                flash('Please provide more detailed feedback or questions (at least 10 characters).', 'danger')
                return render_template('contact.html', form_data=request.form)

            feedback = FeedbackMessage(
                name=name,
                email=email,
                subject=subject,
                category=category,
                message=message,
                status='New'
            )
            db.session.add(feedback)
            db.session.commit()

            flash('Thank you! Your message and feedback have been successfully submitted. Our renewable energy team will get back to you shortly.', 'success')
            return redirect(url_for('contact'))

        return render_template('contact.html', form_data={})

    # =========================================================================
    # AUTHENTICATION
    # =========================================================================
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            location = request.form.get('location', 'Green Valley Community').strip()
            energy_interest = request.form.get('energy_interest', 'Rooftop Solar & Energy Efficiency').strip()

            if not name or len(name) < 2:
                flash('Name must be at least 2 characters long.', 'danger')
                return render_template('register.html', form_data=request.form)

            email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not email or not re.match(email_regex, email):
                flash('Please provide a valid email address.', 'danger')
                return render_template('register.html', form_data=request.form)

            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return render_template('register.html', form_data=request.form)

            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('register.html', form_data=request.form)

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('An account with this email address already exists. Please log in.', 'warning')
                return redirect(url_for('login'))

            user = User(
                name=name,
                email=email,
                location=location or 'Green Valley Community',
                energy_interest=energy_interest,
                role='member'
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email

            flash(f'Welcome to the Community Renewable Energy Portal, {user.name}! Your account has been created.', 'success')
            return redirect(url_for('dashboard'))

        return render_template('register.html', form_data={})

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '').strip()
            next_url = request.args.get('next')

            if not email or not password:
                flash('Please provide both email and password.', 'danger')
                return render_template('login.html', email=email)

            user = User.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                flash('Invalid email or password. Please verify and try again.', 'danger')
                return render_template('login.html', email=email)

            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_role'] = user.role

            flash(f'Welcome back, {user.name}!', 'success')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('dashboard'))

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out securely. See you soon!', 'info')
        return redirect(url_for('index'))

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        user = db.get_or_404(User, session['user_id'])
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            bio = request.form.get('bio', '').strip()
            location = request.form.get('location', '').strip()
            energy_interest = request.form.get('energy_interest', '').strip()

            if not name or len(name) < 2:
                flash('Name cannot be empty.', 'danger')
                return redirect(url_for('profile'))

            user.name = name
            user.bio = bio
            user.location = location
            user.energy_interest = energy_interest
            db.session.commit()

            session['user_name'] = user.name
            flash('Your profile has been updated successfully!', 'success')
            return redirect(url_for('profile'))

        user_posts = CommunityPost.query.filter_by(user_id=user.id).order_by(CommunityPost.created_at.desc()).all()
        user_calculations = SavedCalculation.query.filter_by(user_id=user.id).order_by(SavedCalculation.created_at.desc()).all()
        return render_template('profile.html', user=user, user_posts=user_posts, user_calculations=user_calculations)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
