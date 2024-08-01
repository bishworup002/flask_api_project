from app import create_app, db
from app.models import User, RoleEnum
from sqlalchemy.exc import SQLAlchemyError

def create_user(username, first_name, last_name, email, role, password):
    try:
        if not User.query.filter_by(username=username).first():
            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                role=role
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"User '{username}' created successfully.")
            return True
        else:
            print(f"User '{username}' already exists.")
            return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error creating user '{username}': {str(e)}")
        return False

app = create_app()

with app.app_context():
    # Create admin user
    admin_created = create_user(
        username='admin',
        first_name='Admin',
        last_name='User',
        email='admin@example.com',
        role=RoleEnum.ADMIN,
        password='adminpassword'
    )

    # Create a regular user
    user_created = create_user(
        username='user',
        first_name='Regular',
        last_name='User',
        email='user@example.com',
        role=RoleEnum.USER,
        password='userpassword'
    )

    if admin_created or user_created:
        print("Default users setup completed.")
    else:
        print("No new users were created.")