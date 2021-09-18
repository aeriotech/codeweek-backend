### <span style="color:#00ffff">COOKIFY BACKEND</span>

Backend for the Cookify mobile app, made for a hackaton.

#### BACKEND API
##### /createUser - POST
This endpoint is used to create a new user. It will expect a JSON body with the fields `username` and `password`
Here is what an example request would look like:
```
{
    "username": "Johny",
    "password": "password1"
}
```
A successfull request will return the `userId` with the response code 200. If the JSON is malfored or the username is already taken, the status code 400 is returned.

##### /deleteUser - POST
This endpoint is used to delete an existing user. It will expect a JSON body with the field `userId`.
Here is what an example request would look like:
```
{
    "userId": "2009901c-31bf-4ed9-9294-31bd22637a4b"
}
```
A successfull request will return the `userId` that was deleted with the response code 200. If the JSON is malfored or the user by that id does not eixst, the status code 400 is returned.