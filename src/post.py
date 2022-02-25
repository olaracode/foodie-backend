from flask_pymongo import ObjectId
from flask import request


def create_post(Posts, Users, user):
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
        post["_id"] = str(post["_id"])
        posts.append(post)
    return posts


def get_post(Posts, id):
    post = Posts.find_one({"_id": ObjectId(id)})
    post["_id"] = str(post["_id"])
    return post, 200


# Handle the like and dislike feature within the same function
def handle_likes(Posts, Users, user, id):
    # Define the variables to use
    post = Posts.find_one({"_id": ObjectId(id)})
    post_likes = post["likes"]
    user_likes = user["liked"]
    action = ""

    # Check if the user has already liked the post
    if str(user["_id"]) in post_likes:
        action = "Disliked"
        post_likes.remove(str(user["_id"]))
        user_likes.remove(str(post["_id"]))
    else:
        action = "Liked"
        post_likes.append(str(user["_id"]))
        user_likes.append(str(post["_id"]))

    Posts.update_one({"_id": post["_id"]}, {"$set": {"likes": post_likes}})
    Users.update_one({"_id": user["_id"]}, {"$set": {"liked": user_likes}})

    return {"Msg": "Post {action} successfully".format(action=action)}, 200


def handle_save(Posts, Users, user, id):
    post = Posts.find_one({"_id": ObjectId(id)})
    saved = user["saved"]
    action = ""
    # Check the action to define how to treat the data. Either Append the new items or remove
    if str(post["_id"]) in saved:
        action = "Removed"
        post["saved"] -= 1
        saved.remove(str(post["_id"]))
    else:
        action = "Saved"
        post["saved"] += 1
        saved.append(str(post["_id"]))

    # Update database
    Posts.update_one({"_id": post["_id"]}, {"$set": {"saved": post["saved"]}})
    Users.update_one({"_id": user["_id"]}, {"$set": {"saved": saved}})

    return {"Msg": "Post has been {action} successfully".format(action=action)}, 200


def update_post_categories(Posts, id):
    pass
