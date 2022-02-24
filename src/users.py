from base64 import encode
from posix import environ
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import ObjectId
from flask import request
import jwt
import datetime
import os

# Create a new user


def create_user(Users, request):
    username = request.json["username"]
    name = request.json["name"]
    password = request.json["password"]
    email = request.json["email"]
    gender = request.json["gender"]
    location = request.json["location"]
    # Check if all REQUIRED data is being inputed
    if username and password and email and name and gender and location:
        # Check if the username is taken
        if Users.find_one({"username": username}):
            return {"error": "Username is already taken"}, 401
        elif Users.find_one({"email": email}):
            return {"error": "Email is already in use"}, 401
        elif len(password) < 8:
            return {"error": "Password must be longer than 8 characters"}, 401
        Users.insert_one({
            "username": username,
            "email": email,
            "password": generate_password_hash(password),
            "name": name,
            "gender": gender,
            "location": location,
            "description": "",
            "followers": [],
            "following": [],
            "liked": [],
            "saved": [],
            "profile": ""
        })
        response = {
            "username": username,
            "email": email
        }
        return response, 200


# Get all users
def get_users(Users):
    all_users = Users.find()
    users = []
    for user in all_users:
        users.append({
            "username": user["username"],
            "email": user["email"],
            "_id": str(user["_id"]),
        })
    return users


# Like a post
def add_like_post(id, Users):
    user = Users.find_one({'_id': ObjectId(id)})
    liked_posts = user['liked']
    liked_posts.append(request.json['post_id'])
    Users.update_one({'username': request.json['username']}, {
        '$set': {'liked': liked_posts}
    })
    return {'Msg': "Post liked successfully"}, 200


# List users being followed
def get_following(id, Users):
    user = Users.find_one({"_id": ObjectId(id)})
    following = user["following"]
    following_list = []
    if len(following) == 0:
        return {"Msg": "Not following any users"}
    for followed in following:
        follwd = Users.find_one({"_id": ObjectId(followed)})
        followed_user = {
            "username": follwd["username"],
            "id": followed
            # "profile": user["profile"]
        }
        following_list.append(followed_user)
    return following_list, 200


# List users following current user
def get_followers(id, Users):
    user = Users.find_one({"_id": ObjectId(id)})
    follower_list = []
    followers = user['followers']

    # Check if the user has any followers
    if len(followers) == 0:
        return {"Msg": "No user is following you"}

    # Parse thru followers to create a object-like variable and append it to follower_list
    for follower in followers:
        current_follower = Users.find_one({"_id": ObjectId(follower)})
        follower = {
            "username": current_follower["username"],
            "id": str(current_follower["_id"])
        }
        follower_list.append(follower)

    return follower_list, 200


# Follow
def follow_user(id, Users):
    user = Users.find_one({'_id': ObjectId(id)})
    user_to_follow = Users.find_one(
        {'_id': ObjectId(request.json['user_to_follow'])})

    # Add the user_to_follow to the current user
    following = user['following']

    # Check to see if user is being already followed
    if str(user_to_follow["_id"]) in following:
        return {'Error': 'User is already being followed'}, 401

    following.append(str(user_to_follow["_id"]))

    # Add the current user to the user_to_follow followers list
    followers = user_to_follow['followers']
    followers.append(str(user["_id"]))

    # Updating in database
    Users.update_one({'_id': ObjectId(id)}, {
        '$set': {'following': following}
    })

    Users.update_one({'_id': ObjectId(request.json['user_to_follow'])}, {
        '$set': {'followers': followers}
    })
    return {'Msg': "User followed successfully"}, 200


# Unfollow
def unfollow_user(id, Users):
    user = Users.find_one({'_id': ObjectId(id)})
    user_to_unfollow = Users.find_one(
        {'_id': ObjectId(request.json['user_to_unfollow'])})

    # remove the user_to_unfollow from following list
    following = user['following']
    following.remove(str(user_to_unfollow["_id"]))

    # remove self from user_to_unfollow followers list
    followers = user_to_unfollow["followers"]
    followers.remove[str(user["_id"])]

    # Update Database
    Users.update_one({'_id': ObjectId(id)}, {'$set': {'following': following}})

    Users.update_one({'_id': user_to_unfollow["_id"]}, {
                     '$set': {"followers": followers}})
    return {'Msg': 'User unfollowed successfully'}, 200


# LOGIN
def log_user(Users):
    password = request.json["password"]
    username = request.json["username"]
    if password and username:
        user = Users.find_one({"username": username})
        if user:
            if check_password_hash(user["password"], password):
                token = jwt.encode({'id': str(user["_id"]), "exp": datetime.datetime.now(
                    datetime.timezone.utc) + datetime.timedelta(minutes=30)}, os.environ.get("SECRET_KEY"), algorithm='HS256')
                print(token)
                return token
