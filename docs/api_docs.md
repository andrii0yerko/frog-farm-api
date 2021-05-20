# Authentication
[Basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) is used, so auth-required requests should include header `Authorization: Basic {{credentials}}`, where `{{credentials}}` is Base64 encoded string `<email:password>` or `<username:password>`.

## Check credentials
- **URL**: `/api/v1/auth`

- **Method**: `GET`

- **Auth required**: Yes - request should include `Authorization` header

### Success Response
- **Condition**: Signed in succefully - username(email) exists and password is correct

- **Code**: `200 OK`

- **Content**:
```js
{
    "id": 1,
    "username": "Admin",
    "frogs": "/api/v1/users/1/frogs",
    "money": 900
}
```
### Error Response
Otherwise. All the auth-required requests return the same response if auth was failed.
- **Code**: `401 UNAUTHORIZED`

- **Content**: 
```js
{
    "error": "Unauthorized"
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

## Wash/Feed/Collect income
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

### Success Response
- **Condition**: Frog with requested id exists on the server and the user is its owner.

- **Code**: `200 OK`

- **Content example**:
```js
{
    "id": 2,
    "url": "/api/v1/frogs/2",
    "name": "Большой Поедатель Бутонов",
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
    "frogs": "/api/v1/users/1/frogs"
}
```
Or if signed in as the same user
```js
{
    "id": 1,
    "username": "Admin",
    "frogs": "/api/v1/users/1/frogs",
    "money": 900
}
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
    "frogs": "/api/v1/users/2/frogs"
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
        "cleanliness": 93,
        "food": 80,
        "id": 3,
        "image": "/api/v1/images/3",
        "money": 50,
        "name": "Королевский Милашка",
        "url": "/api/v1/frogs/3"
    },
    {
        "cleanliness": 60,
        "food": 10,
        "id": 4,
        "image": "/api/v1/images/4",
        "money": 50,
        "name": "Вонючий Сфера",
        "url": "/api/v1/frogs/4"
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
