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

> Saved and Sent are set as incremental integers to protect user data

- user-id = _ObjectId_
- username = _String_
- title = _String_
- img = _String(url)_
- ingredients = _String_
- preparation = _Text_
- time = _String_
- servings = _String_
- categories = _Array[Strings]_
- comments = _Array[id's]_
- likes = _Array[id's]_
- saved = _Integer(Incremental)_
- sent = _Integer(Incremental)_

<br/>

## Endpoints

### Users

<br/>

Get user by _id_ **/user/{ id }**

```
Method: Get

Params:
- id: User id

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

Get followed **/user/{ id }/followed**

```
Method: Get

Params:
- id: User_id

Return:
- Response = { [users_followed] }
```

<br/>

Get followers **/user/{ id }**

```
Method: Get

Params:
- id: User_id

Return:
- Response = { [followers] }
```

<br/>

Follow user **/user/{ id }/follow**

```
Method: Post

Params:
- id: User_id

Request:
- user_to_follow = _id

Return:
- Response = { Message }
```

<br/>

Unfollow user **/user/{ id }/follow**

```
Method: Post

Params:
- id: User_id

Request:
- user_to_unfollow = _id

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

Create new post **/post/{ id }/new**

```
Method: Post

Params:
- id: User_id

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
