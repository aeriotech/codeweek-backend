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

##### /login - POST
This endpoint is used to generate an access token from the username and password. It will expect a JSON body with the fields `username` and `password`.
Here is what an example request would look like:
```
{
    "username": "Johny",
    "password": "password1"
}
```
A successfull request will return the `accessToken` with the response code 200. If the JSON is malfored, the status code 400 is returned. If the username or password are incorrect then the status code 401 is returned.

## Authentication
Most requests here require authentication. This is done with Bearer token authentication, You aquire the bearer token with the **/login** endpoint.

##### /items - GET
This endpoint is used to get all the items the logged in user owns
It returns a JSON array with EAN codes and expiration dates

##### /items/new - POST
This endpoint allows the user to add new items to their collection
It expects a JSON body with the the EAN code and expiration date in UNIX timecode flavour, the expiration date is optional, though.
An example request looks like:
```
{
    "ean":"564543755",
    "expiration":"11335535"
}
```
Here you can use the number parameter to set the amount of items of the same type and expiration date that'll be inserted
It returns a code 200, if the item was succesfully added.

##### /items/delete - POST
This endpoint allows the user to delete their items by item ID
It takes a JSON body with the itemID
Example:
```
{
    "itemId":"1"
}
```
**Note:** The user can only delete their own items.
It returns a 200 if the item was deleted succesfully

##### /user/points - GET
This endpoint simply returns the amount of points the user has.
It returns a JSON string
Example:
```
{
    "userId":"54636-5765834-68587",
    "points":69
}
```

##### /user/points/add/x - GET
This endpoint allows for the modification of a users points
Substitute the X in the URL for the number of points you'd like to add.
This number CAN negative
It returns the new number of points the user has
**Note:** The amount of points cannot go under 0, regardless of user input

##### /user/username - GET
This endpoint simply returns the users username in JSON flavour
Example:
```
{
    "userId":"ru64hf5-543v45g-54gg",
    "username":"polde"
}
```
##### /user/premium - GET
Tells you if the logged in user has Premium access
Example response:
```
{
    "userId":"u98ff-f4ff4-f4gf",
    "premium":true
}
```
##### /recipes - GET
Returns all of the recipes the user can see. What this means is that non-premium users do not get the premium recipes.
Here, you can use GET params to filter the recipes by ingredients.
For instance, you can do `/recipes?ingredients=milk,eggs`, and you'll only recieve the recipes that contain milk and eggs.

EXAMPLE TBA

##### /recipes/id - GET
Allows you to access a specific recipe by its ID
Returns JSON for the recipe

EXAMPLE TBA

**Note:** A non-premium user CANNOT get premium recipes, even by ID

##### /recipe/create - POST
Allows you to create new recipess
Expects a JSON body:
```
{
    "name":"chonk",
    "imgUrl":"test",
    "ingredients":"[\"milk\", \"eggs\"]",
    "url":"wooorld",
    "procedure":"maarm",
    "vegan":false,
    "premium":true
}
```
Returns OK if succesfully added

##### /ean/code - GET
**This endpoint doesn't require autentication**
Substitute code with a valid EAN code and get a JSON response


##### /recipes/delete/id - GET
Substitute id for a valid recipe ID and delete it.
