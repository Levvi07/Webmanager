## Basic requirements of all requests
- Request must be POST
- Data must be supplied in json format
- An action attribute must be set, for all requests 
- Token is necessary for all requests (except login)
- It's also advised to create a dedicated API user
## Actions

### Login
| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| username | A username for a regular user | admin | x |
| password | A password for a regular user | passw | x |

- Returns a token (type str)


```json
{  
    "action": "login",  
    "username":"USERNAME",  
    "password":"PASSWORD"  
}  --> str
```

### Sign out
| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |

- Release the active token for security reasons
- Returns an http code

```json
{  
    "action": "signout",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6"    
}  --> str
```


### Reload Plugins
- Reloads the plugins through the API

### Get User Data
| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | The ID of the searched user | 1 |  |
| Name | The name of the searched user | admin |  |
| Email | The email of the searched user | admin@example.com | |
| Full name | The full name of the searched user | Admin Adminton |  |
| Groups | A group id (only one id at a time) | 1 |  |
| Roles | A role id (only one id at a time) | 1 |  |
| Description | A string of description  (snippets dont work, full text is neededd)| 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 |  |
| IsLoggedIn | Either 0 or 1 shows whether a user is logged in at the moment | 1 |  |

- Used to acquire user data
- One may either use it without arguments, or filter for any of the following attributes:
    - ID
    - Name
    - Email
    - Full name
    - Groups
    - Roles
    - Description
    - IsLoggedIn

### Add User

### Remove User

### Modify User
- Not possible to modify password, for safety reasons

### Get Role data

### Add Role

### Remove Role

### Modify Role

### Get Group data

### Add Group

### Remove Group

### Modify Group

### Get site access rule data

### Create a site access rule

### Remove a site access rule

### Modify a site permission rule

### Get config
| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| config | Get the value of one specific config | TokenExpire |  |

### Add config

### Delete config

### Get pluginlist

### Get plugin data

### Enable plugin

### Disable plugin

### Get plugin config

### Add plugin config

### Change plugin config

### Remove plugin config