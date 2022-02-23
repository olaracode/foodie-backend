# Flask Api for Social Media (Foodie)

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

## Endpoints
