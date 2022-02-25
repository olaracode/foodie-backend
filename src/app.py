import jwt
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from itsdangerous import json
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# from utils import generate_random_user
# LOCAL IMPORTS
from users import get_users, create_user, get_following, get_followers, follow_user, log_user, unfollow_user
from post import create_post, get_post, get_user_posts, handle_likes, handle_save

app = Flask(__name__)

load_dotenv()

app.config['MONGO_URI'] = "{uri}".format(uri=os.environ.get("MONGO_URI"))
mongo = PyMongo(app)
db = mongo.db
Users = db.users
Posts = db.posts


# Authentication Middleware
def auth_middleware(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        token = None

        if 'auth_token' in request.headers:
            token = request.headers['auth_token']
        if not token:
            return jsonify({'Msg': 'A valid auth-token is required'})
        try:
            data = jwt.decode(token, options={"verify_signature": False})
            user_auth = Users.find_one(
                {"_id": ObjectId(data['id'])})
        except:
            return jsonify({'mensaje': 'Token invalido'})
        return func(user_auth, *args,  **kwargs)
    return decorador


# < --- USER ROUTES --- >


# Create new user
@app.route('/users/new', methods=['POST'])
def create_new_user():
    response, status = create_user(Users)
    return response, status


# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    response = get_users(Users)
    return jsonify(response)


# Get user By id
# @app.route('/user/<id>', methods=['GET'])
# def get_user(id):
#     user = Users.find_one({'_id': ObjectId(id)})
#     user["_id"] = str(user["_id"])
#     return jsonify(user)


# Get user by username
@app.route('/user/<username>', methods=['GET'])
def get_user_username(username):
    user = Users.find_one({'username': username})
    user["_id"] = str(user["_id"])
    return jsonify(user)


# Login
@app.route('/user/login', methods=["POST"])
def login():
    response = log_user(Users)
    return response


# Update user description
@app.route('/user/<id>/description', methods=['GET'])
def update_description(id):
    Users.update_one({'_id': ObjectId(id)}, {
                     '$set': {'description': request.json['description']}})
    return {'Msg': "User description updated successfully"}, 200


# Get following list. Params: {id: user_id}
@app.route('/user/<id>/followed', methods=['GET'])
def following(id):
    response, status = get_following(id, Users)
    return jsonify(response), status


# Get followers list. Params: {id: user_id}
@app.route('/user/<id>/followers', methods=['GET'])
def followers(id):
    response, status = get_followers(id, Users)
    return jsonify(response), status


# Follow. Params: {id: user_to_follow_id}
@app.route('/user/follow/<id>', methods=['POST'])
@auth_middleware
def follow(user_auth, id):
    response, status = follow_user(Users, user_auth, id)
    return response, status


# Unfollow. Params: {id: user_to_unfollow_id}
@app.route('/user/unfollow/<id>', methods=['POST'])
@auth_middleware
def unfollow(user_auth, id):
    response, status = unfollow_user(Users, user_auth, id)
    return response, status


# < --- POST ROUTES --- >

# Create new post
@app.route('/post/new', methods=["POST"])
@auth_middleware
def post(user_auth):
    response = create_post(Posts, Users, user_auth)
    return jsonify(response)


# Get all posts from user. Params: {id: user_id}
@app.route('/posts/<id>', methods=["GET"])
def user_posts(id):
    response = get_user_posts(Posts, id)
    return jsonify(response)


# Get post by id
@app.route('/post/<id>', methods=["GET"])
def get_post_info(id):
    response = get_post(Posts, id)
    return jsonify(response)


# Like a post. Params: {id: post_id}
# Function handles like and dislike
@app.route('/post/like/<id>', methods=["POST"])
@auth_middleware
def like_post(auth_user, id):
    response, status = handle_likes(Posts, Users, auth_user, id)
    return response, status


@app.route('/post/save/<id>', methods=['POST'])
@auth_middleware
def save_post(auth_user, id):
    response, status = handle_save(Posts, Users, auth_user, id)
    return response, status


# POPULATE DATABASE ¡------ Caution ------!
# @app.route('/populate/users/<count>', methods=['POST'])
# Count works to choose how many new users are going to be created
# def populate(count):
#     new_users = []
#     for i in range(int(count)):
#         new_user = generate_random_user()
#         Users.insert_one({
#             "username": new_user["username"],
#             "email": new_user["email"],
#             "password": generate_password_hash(new_user["password"]),
#             "name": new_user["name"],
#             "gender": new_user["gender"],
#             "location": new_user["location"],
#             "description": "",
#             "followers": [],
#             "following": [],
#             "liked": [],
#             "saved": [],
#             "profile": ""
#         })
#         response = {
#             "username": new_user["username"],
#             "email": new_user["email"]
#         }
#         new_users.append(response)
#     return jsonify(new_users), 200
if __name__ == "__main__":
    app.run(debug=True)
