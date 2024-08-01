from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, RoleEnum
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_bp = Blueprint('user', __name__, url_prefix='/user')

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

# User CRUD operations
@user_bp.route('/<int:user_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def modify_user(user_id):
    current_user = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    if current_user['role'] != 'Admin' or user.role == RoleEnum.ADMIN:
        return jsonify({"msg": "Not authorized to modify this user"}), 403

    if request.method == 'PUT':
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.active = data.get('active', user.active)
        db.session.commit()
        return jsonify({"msg": "User updated successfully"}), 200

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted successfully"}), 200
