from flask_pymongo import ObjectId
from flask import request


def create_post(Posts, Users, id):
    user = Users.find_one({"_id": ObjectId(id)})
    title = request.json["title"]
    img = "img_url"
    ingredients = request.json["ingredients"]
    preparation = request.json["preparation"]
    for i in range(5):
        preparation += preparation
    time = request.json["time"]
    servings = request.json["servings"]
    categories = request.json["categories"]
    if title and img and ingredients and time and servings and categories and preparation:
        # Check if preparation is at least 50 characters long
        if len(preparation) < 15:
            return {"Msg": "Preparation Too short"}, 402

        Posts.insert_one({
            "user_id": str(user["_id"]),
            "username": user["username"],
            "title":  title,
            "img": img,
            "ingredients": ingredients,
            "preparation": preparation,
            "time": time,
            "servings": servings,
            "categories": categories,
            "comments": [],
            "likes": [],
            "saved": 0,
            "sent": 0,
        })
        print("here")
        return {"Msg": "Success"}


# Get all post from a user
def get_user_posts(Posts, id):
    user_posts = Posts.find({"user_id": id})
    posts = []
    for post in user_posts:
        posts.append({
            "title": post["title"],
            "username": post["username"]
        })
    return posts

# def update_post(Posts, id):
