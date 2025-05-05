from app import create_app, db
from app.models import User, Profile, Favourite, Report
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_data():
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        # Get all data from SQLite
        users = User.query.all()
        profiles = Profile.query.all()
        favourites = Favourite.query.all()
        reports = Report.query.all()
        
        # Store the data
        user_data = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'name': user.name,
            'photo': user.photo,
            'date_joined': user.date_joined
        } for user in users]
        
        profile_data = [{
            'id': profile.id,
            'user_id_fk': profile.user_id_fk,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_colour': profile.fav_colour,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented,
            'created_at': profile.created_at,
            'is_complete': profile.is_complete,
            'photo': profile.photo
        } for profile in profiles]
        
        favourite_data = [{
            'id': fav.id,
            'user_id_fk': fav.user_id_fk,
            'fav_user_id_fk': fav.fav_user_id_fk,
            'created_at': fav.created_at
        } for fav in favourites]
        
        report_data = [{
            'id': report.id,
            'reporter_id_fk': report.reporter_id_fk,
            'reported_user_id_fk': report.reported_user_id_fk,
            'reason': report.reason,
            'created_at': report.created_at
        } for report in reports]
        
        # Switch to PostgreSQL database
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        db.session.remove()
        db.get_engine().dispose()
        
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Import data to PostgreSQL
        for user in user_data:
            new_user = User(**user)
            db.session.add(new_user)
        
        # Commit users first
        db.session.commit()
        
        # Now add profiles
        for profile in profile_data:
            new_profile = Profile(**profile)
            db.session.add(new_profile)
        
        # Commit profiles
        db.session.commit()
        
        # Add favourites
        for favourite in favourite_data:
            new_favourite = Favourite(**favourite)
            db.session.add(new_favourite)
        
        # Add reports
        for report in report_data:
            new_report = Report(**report)
            db.session.add(new_report)
        
        # Final commit
        db.session.commit()
        
        print("Migration completed successfully!")

if __name__ == '__main__':
    migrate_data() 