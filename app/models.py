from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(200))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    profiles = db.relationship('Profile', backref='user', lazy='dynamic')
    favorites = db.relationship('Favourite', foreign_keys='Favourite.user_id_fk', backref='user')
    favorited_by = db.relationship('Favourite', foreign_keys='Favourite.fav_user_id_fk', backref='favorite_user')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'photo': self.photo,
            'date_joined': self.date_joined.isoformat() if self.date_joined else None
        }
    
    def has_complete_profile(self):
        """Check if user has at least one complete profile"""
        return self.profiles.filter_by(is_complete=True).first() is not None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    parish = db.Column(db.String(100), nullable=False)
    biography = db.Column(db.Text, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    fav_cuisine = db.Column(db.String(100), nullable=False)
    fav_colour = db.Column(db.String(50), nullable=False)
    fav_school_subject = db.Column(db.String(100), nullable=False)
    political = db.Column(db.Boolean, nullable=False)
    religious = db.Column(db.Boolean, nullable=False)
    family_oriented = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_complete = db.Column(db.Boolean, default=False)
    photo = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id_fk,
            'description': self.description,
            'parish': self.parish,
            'biography': self.biography,
            'sex': self.sex,
            'race': self.race,
            'birth_year': self.birth_year,
            'height': self.height,
            'fav_cuisine': self.fav_cuisine,
            'fav_colour': self.fav_colour,
            'fav_school_subject': self.fav_school_subject,
            'political': self.political,
            'religious': self.religious,
            'family_oriented': self.family_oriented,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_complete': self.is_complete,
            'photo': self.photo
        }
    
    def check_completeness(self):
        """Check if all required fields are filled out"""
        required_fields = [
            self.description, self.parish, self.biography,
            self.sex, self.race, self.birth_year,
            self.height, self.fav_cuisine, self.fav_colour,
            self.fav_school_subject, self.political is not None,
            self.religious is not None, self.family_oriented is not None
        ]
        self.is_complete = all(required_fields)
        return self.is_complete

class Favourite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id_fk', 'fav_user_id_fk', name='unique_favorite'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id_fk,
            'fav_user_id': self.fav_user_id_fk,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    reporter_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reported_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reporter = db.relationship('User', foreign_keys=[reporter_id_fk], backref='reports_made')
    reported_user = db.relationship('User', foreign_keys=[reported_user_id_fk], backref='reports_received')
    
    def to_dict(self):
        return {
            'id': self.id,
            'reporter_id': self.reporter_id_fk,
            'reported_user_id': self.reported_user_id_fk,
            'reporter_name': self.reporter.name if self.reporter else None,
            'reported_user_name': self.reported_user.name if self.reported_user else None,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Report {self.id}: {self.reporter_id_fk} -> {self.reported_user_id_fk}>' 