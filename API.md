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
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
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

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |

- Reloads the plugins through the API
- Returns an HTTP code

```json
{  
    "action": "reload_plugins",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6"
}  --> str
```

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
| Description | A string of description  (snippets dont work, full text is neededd)| Description |  |
| IsLoggedIn | Either 0 or 1 shows whether a user is logged in at the moment | 1 |  |
| API_access | 1 or 0; Whether the user has access to the API | 1 | x |

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

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| Name | The name of the searched user | admin | x |
| Email | The email of the searched user | admin@example.com | x |
| Full name | The full name of the searched user | Admin Adminton | x |
| Password | A password | 1 | x |
| Groups | A group id (only one id at a time) | 1 |  |
| Roles | A role id (only one id at a time) | 1 |  |
| Description | A string of description  (snippets dont work, full text is needed)| Description |  |
| API_access | 1 or 0; Whether the user has access to the API | 1 | x |



### Remove User

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | A valid user id | 1 | x |

### Modify User

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | A valid user id | 1 | x |
| Name | The name of the searched user | admin |  |
| Email | The email of the searched user | admin@example.com |  |
| Full name | The full name of the searched user | Admin Adminton |  |
| Groups | A group id (only one id at a time) | 1 |  |
| Roles | A role id (only one id at a time) | 1 |  |
| Description | A string of description  (snippets dont work, full text is neededd)| Description |  |
| API_access | 1 or 0; Whether the user has access to the API | 1 | x |

- Set fields get modified, unset fields stay the same
- Not possible to modify password, for safety reasons

### Get Role data

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | A valid role id | 1 |  |
| Name | The name of the searched role | admin |  |
| Perm_level | The perm level of the role | 5+ |  |
| Description | A string of description  (snippets dont work, full text is neededd)| Description |  |

- When searching by perm level 3 filters are availabe:
    - `1` means the `perm_level==1`
    - `1+` means the `perm_level>=1`
    - `1-` means the `perm_level<=1`

### Add Role

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| Name | The name of the searched role | admin | x |
| Perm_level | The perm level of the role | 5 |  |
| Description | A string of description  (snippets dont work, full text is neededd)| Description |  |

- When Perm_level is not set it defaults to -1

### Remove Role

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | The ID of the searched role | admin | x |

### Modify Role

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | The ID of the searched role | admin | x |
| Name | The name of the searched role | admin |  |
| Perm_level | The perm level of the role | 5 |  |
| Description | A string of description  (snippets dont work, full text is needed)| Description |  |

- Set fields get modified, unset fields stay the same

### Get Group data

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | A valid group id | 1 |  |
| Name | The name of the searched group | admin |  |
| Perm_level | The perm level of the group | 5+ |  |
| Description | A string of description  (snippets dont work, full text is neededd)| Description |  |

- When searching by perm level 3 filters are availabe:
    - `1` means the `perm_level==1`
    - `1+` means the `perm_level>=1`
    - `1-` means the `perm_level<=1`

### Add Group

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| Name | The name of the searched group | admin | x |
| Perm_level | The perm level of the group | 5 |  |
| Description | A string of description  (snippets dont work, full text is neededd)| Description |  |

- When Perm_level is not set it defaults to -1

### Remove Group

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | The ID of the searched group | admin | x |

### Modify Group

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | The ID of the searched group | admin | x |
| Name | The name of the searched group | admin |  |
| Perm_level | The perm level of the group | 5 |  |
| Description | A string of description  (snippets dont work, full text is needed)| Description |  |

- Set fields get modified, unset fields stay the same

### Get site access rule data

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| endpoint | The endpoint | /admin/* | x |

### Create a site access rule

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| endpoint | The endpoint | /admin/* | x |
| AccessLevel | A number that sets the permission level one must have to access this endpoint | /admin/* | x |
| access_roles_id | A group of roleids that may be granted access (role1;role2;role3) | /admin/* |  |
| access_groups_id | A group of groupids that may be granted access | group1;group2;group3 |  |
| access_users_id | A group of user ids that may be granted access | user1;user2;user3 |  |
| perm_level | sets the access mode of  the endpoint (see docs) | 1 | x |


### Remove a site access rule

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| endpoint | The endpoint | /admin/* | x |

### Modify a site permission rule

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| endpoint | The endpoint | /admin/* | x |
| AccessLevel | A number that sets the permission level one must have to access this endpoint | /admin/* |  |
| access_roles_id | A group of roleids that may be granted access (role1;role2;role3) | /admin/* |  |
| access_groups_id | A group of groupids that may be granted access | group1;group2;group3 |  |
| access_users_id | A group of user ids that may be granted access | user1;user2;user3 |  |
| perm_level | sets the access mode of  the endpoint (see docs) | 1 |  |

- Endpoints are not to be modified, create a new rule for that
- Set fields get modified, unset fields stay the same

### Get config

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| config | Get the value of one or more specific configs | TokenExpire;UserDisabledSite |  |

- In order to retrieve multiple pieces of config seperate the names with semicolons, in that case the api will return a json object

### Add config

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| key | Set the key of the new config | NewConfig | x |
| value | Set the value of the new config | 15 | x |

### Delete config

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| key | Set the key of the new config | NewConfig | x |

### Change config

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| key | Set the key of the new config | NewConfig | x |
| value | Set the value of the new config | 15 | x |

### Get pluginlist

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |

- Returns a list of ALL the plugins

### Get plugin data

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| name | A plugin's name | Template_plugin;plugin2;plugin3 | x |

- Returns data about 1 or more plugins as seperate objects => [{data1},{data2},{data3}]

### Change plugin status

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| name | A plugin's name | Template_plugin;plugin2;plugin3 | x |
| enabled | See below | 1 |  |

- "enabled" field =>
    - 0: Disabled
    - 1: Enabled
    - Left empty: Status gets flipped, if plugin was enabled it gets disabled, if it was disabled it gets enabled 

### Add plugin config

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| name | A plugin's name | Template_plugin;plugin2;plugin3 | x |
| key | Set the key of the new config | NewConfig | x |
| value | Set the value of the new config | 15 | x |

### Change plugin config

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| name | A plugin's name | Template_plugin;plugin2;plugin3 | x |
| key | Set the key of the new config | NewConfig | x |
| value | Set the value of the new config | 15 | x |

### Remove plugin config

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| name | A plugin's name | Template_plugin;plugin2;plugin3 | x |
| key | Set the key of the new config | NewConfig | x |