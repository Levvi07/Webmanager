## Basic requirements of all requests
- Request must be POST
- Data must be supplied in json format
- An action attribute must be set, for all requests 
- Token is necessary for all requests (except login)
- Its also advised to create a dedicated API user
## Actions

### Login
| Name | Description | Example |
| ---- | ----------- | ------- |
| username | A username for a regular user | admin |
| password | A password for a regular user | passw |

- Returns a token (type str)

```
{  
    "action": "login",  
    "username":"USERNAME",  
    "password":"PASSWORD"  
}  --> str
```