from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, RoleEnum
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
try:
    from .config import Config
except ImportError as e:
    print(f"ImportError: {e}")
    raise

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Create a serializer for generating secure tokens
serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

# Register User
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Missing username or password"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 400
    
    user = User(
        username=data['username'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        role=RoleEnum.USER
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

# Sign In User
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role.name})
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

# Password Reset
@auth_bp.route('/reset_password', methods=['POST'])
@jwt_required()
def reset_password():
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    if user and user.check_password(data['old_password']):
        user.set_password(data['new_password'])
        db.session.commit()
        return jsonify({"msg": "Password updated successfully"}), 200
    
    return jsonify({"msg": "Invalid password"}), 400

# Forget Password
@auth_bp.route('/forget_password', methods=['POST'])
def forget_password():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user:
        token = serializer.dumps(user.email, salt='password-reset-salt')
        reset_url = url_for('auth.reset_password_with_token', token=token, _external=True)
        
        return jsonify({
            "msg": "Password reset link generated successfully",
            "reset_link": reset_url
        }), 200
    
    return jsonify({"msg": "Email not found"}), 404

# Reset Password with Token
@auth_bp.route('/reset_password/<token>', methods=['POST'])
def reset_password_with_token(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # Token expires after 1 hour
    except SignatureExpired:
        return jsonify({"msg": "The password reset link has expired"}), 400
    except:
        return jsonify({"msg": "The password reset link is invalid"}), 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        data = request.get_json()
        new_password = data.get('new_password')
        if new_password:
            user.set_password(new_password)
            db.session.commit()
            return jsonify({"msg": "Your password has been updated"}), 200
        else:
            return jsonify({"msg": "New password is required"}), 400
    
    return jsonify({"msg": "User not found"}), 404

# User CRUD operations
@user_bp.route('/<int:user_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def modify_user(user_id):
    current_user = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    # if current_user['role'] != 'Admin' or user.role == RoleEnum.ADMIN:
    #     return jsonify({"msg": "Not authorized to modify this user"}), 403
    # f"{current_user['role'].upper(),RoleEnum.ADMIN.value}"
    if current_user['role'].upper() != RoleEnum.ADMIN.value :
        return jsonify({"msg": "Not authorized to modify this user"}), 403
    if  user.role.value == RoleEnum.ADMIN.value and user.username!=current_user['username']:
        return jsonify({"msg": "You can not change other admin"}), 403
    if request.method == 'PUT':
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.active = data.get('active', user.active)
        # Allow updating role
        new_role = data.get('role').upper()
        if new_role:
            try:
                user.role = RoleEnum(new_role)
            except ValueError:
                return jsonify({"msg": "Invalid role provided"}), 400
        db.session.commit()
        return jsonify({"msg": "User updated successfully"}), 200
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted successfully"}), 200