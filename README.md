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
A successfull request will return the `userId` with the response code 200. If the JSON is malfored, the status code 400 is returned.