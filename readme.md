# Flask Api for Social Media (Foodie)

This API is being created to be consumed by Foodie, a personal React-Native project.

This project uses Flask for the server, Pymongo for the db integration, jwt for authentication purposes, MongoAtlas for cloud hosting of the db, and Cloudinary to store multimedia content.

**_Getting started_**

First clone the repository into your desired location. Then you need to create a Virtual Enviroment, to do so use:

```
# Install virtualenv
pip install virtualenv

# Create a new virtual enviroment
virtualenv -p python3 venv

# To start the virtual enviroment Linux & Mac
source ./venv/bin/activate
```

Afterwards you need to install flask and its dependancies

```
# Install flask
pip install requirements.txt

# Start flask
python3 src/app.py
```

Then you need to create a **.env** file to store your mongo connection string and Cloudinary set up

```
touch .env
```

Inside your .env file you need to declare first and foremost the MONGO_URI, which you can get from mongodb.com using their cloudstorage service. You can find a guide on how to create a mongo cluster and get the Connection string in [here](https://studio3t.com/knowledge-base/articles/connect-to-mongodb-atlas/)

Your .env file should end up looking something like:

```
MONGO_URI=your_mongo_connection_string
```

This api should be easy to customize considering that Mongodb models are not forced upon the database nor server. Which means that you can change them as the project develops or as needs surges.

## Db Models

> Since we use MongoDb this models just work as a guide

**User**

- \_id
- username - _String_
- name - _String_
- password - _String[Hashed]_
- email - _String_
- gender - _String_
- location - _String_
- description - _String_
- followers - _Array[id's]_
- following - _Array[id's]_
- liked - _Array[id's]_
- saved - _Array[id's]_
- profile-img - _String(url)_

**Posts**

- user-id = _ObjectId_
- username = _String_
- title = _String_
- img = _String(url)_
- ingredients = _Array[Strings]_
- preparation = _Text_
- time = _String_
- servings = _String_
- categories = _Array[Strings]_
- comments = _Array[id's]_
- likes = _Array[id's]_
- saved = _Integer(Incremental)_
- sent = _Integer(Incremental)_

> Saved and Sent are set as incremental integers to protect user data

<br/>

## Endpoints

### Users

<br/>

Get user by username **/user/{ username }**

```
Method: Get

Params:
- username

Return:
- { user }
```

<br/>

Create a new User **/users/new**

```
Method: Post

Request:
- username
- name
- password
- password_confirm
- email
- gender
- location

Return:
- Response = {username, email}
```

<br/>

Get users **/users**

```
Method: Get

Return:
- Response = { [users] }
```

<br/>

Get followed **/user/followed/{ id }**

```
Method: Get

Params:
- id: User ID

Return:
- Response = { [users_followed] }
```

<br/>

Get followers **/user/followers/{ id }**

```
Method: Get

Params:
- id: User ID

Return:
- Response = { [followers] }
```

<br/>

Follow user **/user/follow/{ id }**

```
Method: Post

Headers:
- user_auth: jwt_token

Params:
- id: User to follow ID

Return:
- Response = { Message }
```

<br/>

Unfollow user **/user/follow/{ id }**

```
Method: Post

Headers:
- user_auth: jwt_token

Params:
- id: User to unfollow ID

Return:
- Response = { Message }
```

### Posts

<br>

Get user posts **/posts/{ id }/**

```
Method: Get

Params:
- id: user_id

Returns:
- { [user_posts] }
```

<br/>

Create new post **/post/new**

```
Method: Post

Headers:
- user_auth: jwt_token

Request:
- user
- title
- img
- ingredients
- preparation
- time
- servings
- categories

Return:
- Response = { Message }
```

<br/>

Like post **/post/like/{ id }**

```
Method: Post

Params:
- id: Post ID

Headers:
- user_auth: jwt_token

Return:
- Response = { Message }
```

<br/>

Disike post **/post/dislike/{ id }**

```
Method: Post

Params:
- id: Post ID

Headers:
- user_auth: jwt_token

Return:
- Response = { Message }
```

<br/>

Update a post **/post/update/{ id }**

```
Method: PUT

Params:
- id: Post ID

Headers:
- user_auth: jwt_token

Request:
- Title
- Preparation
- Ingredients
- Categories
- Servings
- Time

Return:
- Response = { Message }
```
