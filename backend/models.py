import py_loader
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def utc_now():
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='member')  # 'member' or 'admin'
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), default='Community Member')
    energy_interest = db.Column(db.String(100), default='Rooftop Solar & Efficiency')
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    posts = db.relationship('CommunityPost', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('PostComment', backref='author', lazy=True, cascade='all, delete-orphan')
    calculations = db.relationship('SavedCalculation', backref='user', lazy=True)
    proposed_projects = db.relationship('Project', backref='creator', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Solar, Wind, Hydro, Biomass, Microgrid
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.String(60), nullable=False)  # e.g., "450 kW", "1.2 MW"
    annual_generation = db.Column(db.Float, default=0.0)  # MWh per year
    co2_saved_annual = db.Column(db.Float, default=0.0)  # Metric tons CO2/year
    participants_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(30), default='Active')  # Active, Planning, Completed
    budget = db.Column(db.Float, default=0.0)
    installation_guide = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    def __repr__(self):
        return f"<Project {self.title}>"


class CommunityPost(db.Model):
    __tablename__ = 'community_posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='Solar Experience')  # Solar Experience, Wind & DIY, Biomass, Energy Tips, General Discussion
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)

    comments = db.relationship('PostComment', backref='post', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<CommunityPost {self.title}>"


class PostComment(db.Model):
    __tablename__ = 'post_comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    def __repr__(self):
        return f"<PostComment {self.id}>"


class SavedCalculation(db.Model):
    __tablename__ = 'saved_calculations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    monthly_bill = db.Column(db.Float, nullable=False)
    monthly_kwh = db.Column(db.Float, nullable=False)
    tariff_rate = db.Column(db.Float, default=0.15)
    roof_area_sqft = db.Column(db.Float, default=500.0)
    sunlight_hours = db.Column(db.Float, default=5.0)
    recommended_kw = db.Column(db.Float, nullable=False)
    monthly_savings = db.Column(db.Float, nullable=False)
    annual_savings = db.Column(db.Float, nullable=False)
    co2_reduction_tons = db.Column(db.Float, nullable=False)
    trees_equivalent = db.Column(db.Integer, default=0)
    payback_years = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=utc_now)

    def __repr__(self):
        return f"<SavedCalculation {self.id} - ${self.annual_savings}/yr>"


class FeedbackMessage(db.Model):
    __tablename__ = 'feedback_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), default='General Feedback')  # Inquiry, Suggestion, Project Collaboration, Portal Feedback
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='New')  # New, Reviewed, Resolved
    created_at = db.Column(db.DateTime, default=utc_now)

    def __repr__(self):
        return f"<FeedbackMessage from {self.name}>"


class EnergyTip(db.Model):
    __tablename__ = 'energy_tips'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Home, Kitchen & Appliances, Heating & Cooling, Lighting, Solar Tips
    description = db.Column(db.Text, nullable=False)
    potential_savings_kwh = db.Column(db.Integer, default=50)  # kWh saved per month/year
    difficulty = db.Column(db.String(20), default='Easy')  # Easy, Medium, Advanced
    icon = db.Column(db.String(50), default='bi-lightbulb')

    def __repr__(self):
        return f"<EnergyTip {self.title}>"


class EducationalArticle(db.Model):
    __tablename__ = 'educational_articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Solar, Wind, Hydro, Biomass, Environment
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    read_time = db.Column(db.String(20), default='5 min read')
    icon = db.Column(db.String(50), default='bi-journal-text')
    created_at = db.Column(db.DateTime, default=utc_now)

    def __repr__(self):
        return f"<EducationalArticle {self.title}>"
