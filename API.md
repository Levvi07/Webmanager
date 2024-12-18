## Basic requirements of all requests
- Request must be POST
- Data must be supplied in json format
- An action attribute must be set, for all requests 
- Token is necessary for all requests (except login)

## Actions

### Login
- username: the username the login uses
- password: the password for the login

- Returns a token (type str)

> {
>     "action": "login",
>     "username":"Levi",
>     "password":"tucepI123"
> }
