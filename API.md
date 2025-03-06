## Basic requirements of all requests
- Request must be POST
- Data must be supplied in json format
- An action attribute must be set, for all requests 
- Token is necessary for all requests (except login)
- It's also advised to create a dedicated API user, because tokens get funky when you log in through the web and API at the same time
## Actions

### Login
##### Permission Level: Read (0)
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
##### Permission Level: Read (0)

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
##### Permission Level: Write (1)
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
##### Permission Level: Read (0)

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
| API_access | 1 or 0; Whether the user has access to the API | 1 |  |

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
    - API_access
- Its only possible to search for 1 group and 1 role at a time

```json
{  
    "action": "get_user",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":"1",
    "name":"admin",
    "email":"admin@example.com",
    "full_name":"Admin Adminton",
    "groups":1,
    "roles":2,
    "description":"Is very admin",
    "IsLoggedIn":1,
    "API_access":1
}  --> json
```

### Add User
##### Permission Level: Write (1)

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

```json
{  
    "action": "add_user",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":"1",
    "name":"admin",
    "email":"admin@example.com",
    "full_name":"Admin Adminton",
    "password":"PASSWORD123",
    "groups":[1,2,3],
    "roles":2,
    "description":"Is very admin",
    "API_access":1
}  --> json
```

### Remove User
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | A valid user id | 1 | x |

```json
{  
    "action": "remove_user",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":1
}  --> str
```

### Modify User
##### Permission Level: Write (1)

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
| API_access | 1 or 0; Whether the user has access to the API | 1 |  |

- Set fields get modified, unset fields stay the same
- Not possible to modify password, for safety reasons

```json
{  
    "action": "modify_user",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":"1",
    "name":"admin",
    "email":"admin@example.com",
    "full_name":"Admin Adminton",
    "groups":[1,2,3],
    "roles":2,
    "description":"Is very admin",
    "API_access":1
}  --> str
```

### Get Role data
##### Permission Level: Read (0)

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

```json
{  
    "action": "get_role",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":1,
    "name":"admin",
    "perm_level":2,
    "description":"Admin role"
}  --> json
```

### Add Role
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| Name | The name of the searched role | admin | x |
| Perm_level | The perm level of the role | 5 |  |
| Description | A string of description  (snippets dont work, full text is neededd)| Description |  |

- When Perm_level is not set it defaults to -1

```json
{  
    "action": "add_role",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":1,
    "name":"admin",
    "perm_level":2,
    "description":"Admin role"
}  --> str
```

### Remove Role
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | The ID of the searched role | admin | x |

```json
{  
    "action": "remove_role",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":1
}  --> str
```

### Modify Role
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | The ID of the searched role | admin | x |
| Name | The name of the searched role | admin |  |
| Perm_level | The perm level of the role | 5 |  |
| Description | A string of description  (snippets dont work, full text is needed)| Description |  |

- Set fields get modified, unset fields stay the same

```json
{  
    "action": "modify_role",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":1,
    "name":"admin",
    "perm_level":2,
    "description":"Admin role"
}  --> str
```

### Get Group data
##### Permission Level: Read (0)

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

```json
{  
    "action": "get_group",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":1,
    "name":"admin",
    "perm_level":2,
    "description":"Admin group"
}  --> json
```

### Add Group
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| Name | The name of the searched group | admin | x |
| Perm_level | The perm level of the group | 5 |  |
| Description | A string of description  (snippets dont work, full text is neededd)| Description |  |

- When Perm_level is not set it defaults to -1

```json
{  
    "action": "add_group",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":1,
    "name":"admin",
    "perm_level":2,
    "description":"Admin group"
}  --> str
```

### Remove Group
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | The ID of the searched group | admin | x |

```json
{  
    "action": "remove_group",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":1
}  --> str
```

### Modify Group
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| ID | The ID of the searched group | admin | x |
| Name | The name of the searched group | admin |  |
| Perm_level | The perm level of the group | 5 |  |
| Description | A string of description  (snippets dont work, full text is needed)| Description |  |

- Set fields get modified, unset fields stay the same

```json
{  
    "action": "modify_group",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "ID":1,
    "name":"admin",
    "perm_level":2,
    "description":"Admin group"
}  --> str
```

### Get site access rule data
##### Permission Level: Read (0)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| endpoint | The endpoint | /admin/* | x |

- access_role/groups/users_id must be either a single integer or an arary of them
- When searching by perm level 3 filters are availabe:
    - `1` means the `perm_level==1`
    - `1+` means the `perm_level>=1`
    - `1-` means the `perm_level<=1`

```json
{  
    "action": "get_access_rule",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "endpoint":"/admin/*",
    "AccessLevel":0,
    "access_roles_id":[1,2,3],
    "access_groups_id":1,
    "access_users_id":-1,
    "perm_level":2
}  --> json
```

### Create a site access rule
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| endpoint | The endpoint | /admin/* | x |
| AccessLevel | A number that sets the permission level one must have to access this endpoint | /admin/* | x |
| access_roles_id | A group of roleids that may be granted access (role1;role2;role3) | /admin/* |  |
| access_groups_id | A group of groupids that may be granted access | group1;group2;group3 |  |
| access_users_id | A group of user ids that may be granted access | user1;user2;user3 |  |
| perm_level | sets the access mode of  the endpoint (see docs) | 1 | x |

- access_role/groups/users_id must be either a single integer or an arary of them

```json
{  
    "action": "add_access_rule",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "endpoint":"/admin/*",
    "AccessLevel":0,
    "access_roles_id":[1,2,3],
    "access_groups_id":1,
    "access_users_id":-1,
    "perm_level":2
}  --> str
```

### Remove a site access rule
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| endpoint | The endpoint | /admin/* | x |

```json
{  
    "action": "remove_access_rule",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "endpoint":"/admin/*"
}  --> str
```

### Modify a site permission rule
##### Permission Level: Write (1)

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
- access_role/groups/users_id must be either a single integer or an arary of them

```json
{  
    "action": "add_access_rule",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "endpoint":"/admin/*",
    "AccessLevel":0,
    "access_roles_id":[1,2,3],
    "access_groups_id":1,
    "access_users_id":-1,
    "perm_level":2
}  --> str
```

### Get config
##### Permission Level: Read (0)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| config | Get the value of one or more specific configs | TokenExpire;UserDisabledSite |  |

- In order to retrieve multiple pieces of config use an array, in that case the api will return a json object
- One may also just pass 1 argument for it as a string
- If no argument is passed to it, the API will return all the configs

```json
{  
    "action": "get_config",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "config":["AutoDisable", "LoggingEnabled"]
}  --> json
```

### Add config

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| key | Set the key of the new config | NewConfig | x |
| value | Set the value of the new config | 15 | x |

```json
{  
    "action": "add_config",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "key":"new_config",
    "value":"this is the value"
}  --> str
```

### Delete config
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| key | Set the key of the new config | NewConfig | x |

```json
{  
    "action": "remove_config",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "key":"old_config"
}  --> str
```

### Change config
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| key | Set the key of the new config | NewConfig | x |
| value | Set the value of the new config | 15 | x |

```json
{  
    "action": "change_config",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "key":"new_config",
    "value":"this is the modified value"
}  --> str
```

### Get pluginlist
##### Permission Level: Read (0)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |

- Returns a list of ALL the plugins

```json
{  
    "action": "get_pl_list",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6"    
}  --> json
```

### Get plugin data
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| name | A plugin's name | Template_plugin;plugin2;plugin3 | x |

- Name must be a json array
- Returns data about 1 or more plugins as seperate objects => [{data1},{data2},{data3}]

```json
{  
    "action": "get_pl",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "name": ["plugin1", "plugin2"]
}  --> json
```

### Change plugin status
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| name | A plugin's name | Template_plugin;plugin2;plugin3 | x |
| enabled | See below | 1 |  |

- "enabled" field =>
    - 0: Disabled
    - 1: Enabled
    - Left empty: Status gets flipped, if plugin was enabled it gets disabled, if it was disabled it gets enabled 

```json
{  
    "action": "change_pl_status",
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "name": "plugin1",
    "enabled":0
}  --> str
```

### Add plugin config
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| name | A plugin's name | Template_plugin;plugin2;plugin3 | x |
| key | Set the key of the new config | NewConfig | x |
| value | Set the value of the new config | 15 | x |

```json
{  
    "action": "add_pl_config",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "name": "plugin1",
    "key":"New_key",
    "value":0
}  --> str
```

### Change plugin config
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| name | A plugin's name | Template_plugin;plugin2;plugin3 | x |
| key | Set the key of the new config | NewConfig | x |
| value | Set the value of the new config | 15 | x |

```json
{  
    "action": "change_pl_config",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "name": "plugin1",
    "key":"New_key",
    "value":0
}  --> str
```

### Remove plugin config
##### Permission Level: Write (1)

| Name | Description | Example | Required |
| ---- | ----------- | ------- | :------: |
| token | An active token | 1\|admin\|3c8ce0623a0b56ca7550d170fcefb6 | x |
| name | A plugin's name | Template_plugin;plugin2;plugin3 | x |
| key | Set the key of the new config | NewConfig | x |

```json
{  
    "action": "change_pl_config",  
    "token":"1|admin|3c8ce0623a0b56ca7550d170fcefb6",
    "name": "plugin1",
    "key":"New_key"
}  --> str
```