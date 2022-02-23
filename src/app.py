import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from itsdangerous import json
from werkzeug.security import generate_password_hash, check_password_hash
# from utils import generate_random_user
from users import get_users, create_user, add_like_post, get_following, get_followers, follow_user, unfollow_user
from post import create_post, get_user_posts


app = Flask(__name__)

load_dotenv()

print(os.getenv("MONGO_URI"))
app.config['MONGO_URI'] = "{uri}".format(uri=os.environ.get("MONGO_URI"))
mongo = PyMongo(app)
db = mongo.db
Users = db.users
Posts = db.posts
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
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = Users.find_one({'_id': ObjectId(id)})
    user["_id"] = str(user["_id"])
    return jsonify(user)


# Update user description
@app.route('/user/<id>/description', methods=['GET'])
def update_description(id):
    Users.update_one({'_id': ObjectId(id)}, {
                     '$set': {'description': request.json['description']}})
    return {'Msg': "User description updated successfully"}, 200


# Like a post <------ INCOMPLETE
@app.route('/user/<id>/add/like', methods=['POST'])
def like_post(id):
    add_like_post(id, Users)


# Get following list
@app.route('/user/<id>/following', methods=['GET'])
def following(id):
    response, status = get_following(id, Users)
    return jsonify(response), status


# Get Followers list
@app.route('/user/<id>/followers', methods=['GET'])
def followers(id):
    response, status = get_followers(id, Users)
    return jsonify(response), status


# Follow
@app.route('/user/<id>/follow', methods=['POST'])
def follow(id):
    response, status = follow_user(id, Users)
    return response, status


# Unfollow
@app.route('/user/<id>/unfollow', methods=['POST'])
def unfollow(id):
    unfollow_user(id, Users)


# < --- POST ROUTES --- >
@app.route('/post/<id>/new', methods=["POST"])
def post(id):
    response = create_post(Posts, Users, id)
    return jsonify(response)


@app.route('/posts/<id>', methods=["GET"])
def user_posts(id):
    response = get_user_posts(Posts, id)
    return jsonify(response)


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
