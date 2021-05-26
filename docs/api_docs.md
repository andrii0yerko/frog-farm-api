# Authentication
[JWT authentication](https://en.wikipedia.org/wiki/JSON_Web_Token) is used, so auth-required requests should include header `Authorization: Bearer {{token}}`.

## Get token
- **URL**: `/api/v1/auth`

- **Method**: `POST`

- **Body**:
```
{
    "username": "username or password",
    "password": "password"
}
```

### Success Response
- **Condition**: Signed in succefully - username(email) exists and password is correct

- **Code**: `200 OK`

- **Content**:
```js
{
    "access_token": "token..."
}
```
### Error Response
Otherwise
- **Code**: `401 UNAUTHORIZED`

- **Content**: 
```js
{
    "error": "Unauthorized",
    "message": "Wrong username or email"
    // OR
    "message": "Wrong password"
}
```

## Get current user
- **URL**: `/api/v1/auth`

- **Method**: `GET`

- **Auth required**: Yes

### Success Response
- **Condition**: Auth token is valid

- **Code**: `200 OK`

- **Content**:
```js
{
    "id": 1,
    "username": "Admin",
    "frogs": "/api/v1/users/1/frogs",
    "money": 6302,
    "total_food_spent": 63,
    "total_water_spent": 73,
    "total_money_collected": 130
}
```
### Error response
Otherwise. All the auth-required requests return the same response if auth was failed.

- **Code**: `401 UNAUTHORIZED`

- **Content**:
```js
{
    "error": "Unauthorized",
    "message": "reason why authentication was failed"
}
```

# Images
## Get image
Get specific image from the server
- **URL**: `/api/v1/images/<int:id>`

- **Method**: `GET`

- **Auth required**: No

### Success Response
- **Condition**: Image with requested id exists on the server

- **Code**: `200 OK`

- **Content**: file attached as `image/*`

### Error Response
- **Condition**: Image with requested id does not exist on the server

- **Code**: `404 NOT FOUND`

- **Content**: 
```js
{
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
}
```

## Generate random image
Returns random output of the generative model

- **URL**: `/api/v1/random_image`

- **Method**: `GET`

- **Auth required**: No

### Success Response

- **Code**: `200 OK`

- **Content**: file attached as `image/*`

# Frogs
## Get frog
Get specific frog info from the server

- **URL**: `/api/v1/frogs/<int:id>`

- **Method**: `GET`

- **Auth required**: No

### Success Response
- **Condition**: Frog with requested id exists on the server

- **Code**: `200 OK`

- **Content example**:
```js
{
    "id": 2,
    "url": "/api/v1/frogs/2",
    "name": "Большой Поедатель Бутонов",
    "level": 0,
    "food": 0,
    "money": 100,
    "cleanliness": 0,
    "image": "/api/v1/images/2"
}
```

### Error Response
- **Condition**: Frog with requested id does not exist on the server

- **Code**: `404 NOT FOUND`

- **Content**: 
```js
{
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
}
```

## Wash/Feed/Collect income/Upgrade the frog
Get specific frog info from the server

- **URL**: `/api/v1/frogs/<int:id>`

- **Method**: `PUT`

- **Auth required**: Yes

- **Permissions required**: User is owner of the frog

- **Body**:
```js
{
    "action": "feed"
}
```
OR
```js
{
    "action": "wash"
}
```
OR
```js
{
    "action": "collect"
}
```
OR
```js
{
    "action": "upgrade"
}
```

### Success Response
- **Condition**: Frog with requested id exists on the server and the user is its owner.

- **Code**: `200 OK`

- **Content example**:
```js
{
    "id": 2,
    "url": "/api/v1/frogs/2",
    "name": "Большой Поедатель Бутонов",
    "level": 0,
    "food": 100,
    "money": 100,
    "cleanliness": 0,
    "image": "/api/v1/images/2"
}
```

### Error Response
- **Condition**: Frog with requested id does not exist on the server

- **Code**: `404 NOT FOUND`

- **Content**: 
```js
{
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
}
```
OR

- **Condition**: User does not own this frog

- **Code**: `403 FORBIDDEN`

- **Content**: 
```js
{
    "error": "Forbidden",
    "message": "Not your frog!"
}
```
OR

- **Condition**: The action was "upgrade" but the user does not have enough money

- **Code**: `400 BAD REQUEST`

- **Content**: 
```js
{
    "error": "Bad Request",
    "message": "Not enough money"
}
```

## Delete the frog
Never try to do this

- **URL**: `/api/v1/frogs/<int:id>`

- **Method**: `DELETE`

# Users
## Get user
Get specific user info from the server

- **URL**: `/api/v1/users/<int:id>`

- **Method**: `GET`

- **Auth required**: optional

### Success Response
- **Condition**: User with requested id exists on the server

- **Code**: `200 OK`

- **Content example**:
```js
{
    "id": 1,
    "username": "Admin",
    "frogs": "/api/v1/users/1/frogs",
    "money": 900,
    "total_food_spent": 63,
    "total_water_spent": 73,
    "total_money_collected": 130
}
```

## Search user by username
Get a list of users matching a query

- **URL**: `/api/v1/users?username=<string:query>`

- **Method**: `GET`

- **Auth required**: No

### Success Response

- **Code**: `200 OK`

- **Content example**:
```js
[
    {
        "username": "Admin",
        "url": "/api/v1/users/1"
    },
    {
        "username": "admin1",
        "url": "/api/v1/users/10"
    },
    {
        "username": "not admin",
        "url": "/api/v1/users/26"
    }
]
```
If the query was not specified, a list of all users will be returned.

## Create a new user
- **URL**: `/api/v1/users`

- **Method**: `Post`

- **Auth required**: No

- **Body**:
```js
{
    "username": "New User",  // must be unique
    "email": "lol@lol.lol",  // must be unique and in a correct email format
    "password": "qwerty123"  // at least 8 characters, 1 number and 1 letter
}
```

### Success Response
- **Code**: `201 CREATED`

- **Content example**:
```js
{
    "id": 2,
    "username": "New User",
    "frogs": "/api/v1/users/2/frogs",
    "money": 100,
    "total_food_spent": 0,
    "total_water_spent": 0,
    "total_money_collected": 0
}
```

### Error response
- **Condition**: User with this username or email already exists.

- **Code**: `400 BAD REQUEST`

- **Content**: 
```js
{
    "error": "Bad Request",
    "message": "User with the same username already exists"
    // OR
    "message": "User with the same email already exists"
}
```
OR
- **Condition**: Email or password fails format check.

- **Code**: `400 BAD REQUEST`

- **Content**: 
```js
{
    "message": {
        "email": "Enter a correct email",
        // OR
        "password": "Your password must include minimum eight characters, at least one letter and one number"
    }
}
```

## List of user frogs
Get list of all user frogs from the server

- **URL**: `/api/v1/users/<int:id>/frogs`

- **Method**: `GET`

### Success Response
- **Condition**: User with requested id exists on the server

- **Code**: `200 OK`

- **Content example**:
```js
[
    {
        "id": 1,
        "url": "/api/v1/frogs/1",
        "name": "Круглый Бахрома",
        "level": 0,
        "food": 97,
        "money": 108,
        "cleanliness": 87,
        "image": "/api/v1/images/1"
    },
    {
        "id": 2,
        "url": "/api/v1/frogs/2",
        "name": "Круглый Дождевая лягушка",
        "level": 0,
        "food": 96,
        "money": 100,
        "cleanliness": 0,
        "image": "/api/v1/images/2"
    }
]
```

### Error Response
- **Condition**: User with requested id does not exist on the server

- **Code**: `404 NOT FOUND`

- **Content**: 
```js
{
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
}
```

## Buy a frog

- **URL**: `/api/v1/users/<int:id>/frogs`

- **Method**: `POST`

- **Auth required**: Yes

- **Permissions required**: Signed in as the same user

### Success Response
- **Condition**: User with requested id exists has enough money.

- **Code**: `201 OK`

- **Content example**:
```js
{
    "id": 11,
    "url": "/api/v1/frogs/11",
    "name": "Милашка Бахрома",
    "level": 0,
    "food": 50,
    "money": 0,
    "cleanliness": 50,
    "image": "/api/v1/images/14"
}
```

### Error response
- **Condition**: User does not have enough money

- **Code**: `400 Bad Request`

- **Content**: 
```js
{
    "error": "Bad Request",
    "message": "Not enough money"
}
```
OR

- **Condition**: ID does not match the user's ID

- **Code**: `403 Bad Request`

- **Content**: 
```js
{
    "error": "Forbidden",
    "message": "Not your account!"
}
```
