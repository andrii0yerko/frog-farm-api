# Websockets

As an alternative to REST API through HTTP, gameplay is available through WebSocket connection on `wss://{{url}}/api/v1/gameplay` with its own message format, as specified below.

# Message format
In general, all the messages coming from the client (except the [technical](#technical), watch below) should be JSON-formatted with the following fields
```js
{
    "action": "one of the available actions"
    "...": "additional fields required for this action"
}
```

All the server responses are JSON-formatted too, and can be one of three possible types

**Error message**:
```js
{
    "type": "error",
    "message": "Message explaining the error"
}
```
E. g.
```js
{
    "type": "error",
    "message": "Your message is not JSON-serializable"
}
```

**Info message**:
```js
{
    "type": "info",
    "message": "Useful information"
}
```

**Content messages**:
```js
{
    "type": "content",
    "content_type": "..."
    "payload": {
        // JSON of content object
        // (or list of them)
    }
}
```

# Authorization
For actions other than get, connection should be authorized. It can be done with:
```js
{
    "action":"authorization",
    "username": "username or email",
    "password": "password"
}
```

### Success response
If credentials are valid
```js
{
    "type": "info",
    "message": "Logged in"
}
```

### Error responses
Self-explanatory
```js
{
    "type": "error",
    "message": "Wrong username or email"
}
```
OR
```js
{
    "type": "error",
    "message": "Wrong password"
}
```

Any attempt to send authorization required message through unauthorized connection will be responded with 
```js
{
    "type": "error",
    "message": "You should log in first"
}
```

# Frog actions
## Get a frog
```js
{
    "action":"get",
    "resource": "frog",
    "frog_id": 1
}
```

### Success response
Frog with requested id exists
```js
{
    "type": "content",
    "content_type": "frog",
    "payload": {
        "food": 100,
        "level": 3,
        "id": 1,
        "image": "/api/v1/images/1",
        "money": 50,
        "cleanliness": 50,
        "name": "Круглый Бахрома"
    }
}
``` 

### Error response
Otherwise
```js
{
    "type": "error",
    "message": "There is no frog with such id"
}
```

## Wash/Feed/Collect money/Upgrade a frog
_Authorization required_
```js
{
    "action":"interact",
    "subaction": "wash",  // or "feed", "collect", "upgrade"
    "frog_id": 1
}
```
### Success response
Frog with requested id exists, and action was completed
```js
{
    "type": "content",
    "content_type": "frog",
    "payload": {
        "food": 100,
        "level": 3,
        "id": 1,
        "image": "/api/v1/images/1",
        "money": 50,
        "cleanliness": 50,
        "name": "Круглый Бахрома"
    }
}
```

### Error response
Frog with such id does not exists
```js
{
    "type": "error",
    "message": "There is no frog with such id"
}
```
User does not own this frog
```js
{
    "type": "error",
    "message": "Not your frog"
}
```

The subaction was "upgrade" but the user does not have enough money
```js
{
    "type": "error",
    "message": "Not enough money"
}
```

## Buy a frog
_Authorization required_
```js
{
    "action":"buy"
}
```

### Success response
```js
{
    "type": "content",
    "content_type": "frog",
    "payload": {
        "food": 50,
        "level": 0,
        "id": 2,
        "image": "/api/v1/images/2",
        "money": 0,
        "cleanliness": 50,
        "name": "Милашка Лист"
    }
}
```


### Error response
The user does not have enough money
```js
{
    "type": "error",
    "message": "Not enough money"
}
```

# User
## Current user
_Authorization required_
```js
{
    "action": "get",
    "resource": "me"
}
```
### Success response
```js
{
    "type": "content",
    "content_type": "user",
    "payload": {
        "username": "Admin",
        "id": 1,
        "total_food_spent": 14297,
        "total_water_spent": 14882,
        "money": 2756,
        "total_money_collected": 13011
    }
}
```

## User statistics
```js
{
    "action": "get",
    "resource": "user",
    "user_id": "1"
}
```

### Success response
User with requested id exists
```js
{
    "type": "content",
    "content_type": "user",
    "payload": {
        "username": "Admin",
        "id": 1,
        "total_food_spent": 14297,
        "total_water_spent": 14882,
        "money": 2756,
        "total_money_collected": 13011
    }
}
```

### Error response
Otherwise
```js
{
    "type": "error",
    "message": "There is no user with such id"
}
```

## User frogs
```js
{
    "action": "get",
    "resource": "frogs",
    "user_id": "1"
}
```

### Success response
User with requested id exists
```js
{
    "type": "content",
    "content_type": "frogs",
    "payload": [
        {
            "food": 90,
            "level": 3,
            "id": 1,
            "image": "/api/v1/images/1",
            "money": 130,
            "cleanliness": 60,
            "name": "Круглый Бахрома"
        },
        {
            "food": 67,
            "level": 1,
            "id": 2,
            "image": "/api/v1/images/2",
            "money": 108,
            "cleanliness": 89,
            "name": "Милашка Лист"
        }
    ]
}
```
### Error response
Otherwise
```js
{
    "type": "error",
    "message": "There is no user with such id"
}
```

# Technical
`PING` - message that will not be responded by the server, but can be useful to keep the connection alive
if there are some limitations for the idling time (e.g. 55 seconds on Heroku)

Server -> client ping message currently is not provided, feel free to add it on your own :)