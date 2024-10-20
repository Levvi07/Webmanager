# This is a website hosting my custom server control software
## Rules for changing Site Permissions:
### Set permission level

- -1 = no one may access
- 0 = only accessible by certain users and groups
- 1 = anyone with the set permission level or one above it may access (set with perm_level column, permission level of a user is determined by their highest ranking group or role, except if they have the a role/group with the permission level -1, in which case all endpoints are denied)
- not in the list = accessible to anyone


### Fill out group/rule/user ids

- if -1 is present in user_access_role then the URL must end in an id (eg. /user/1)
in this case the given id may be provided access too

/dir/dir2/* means anything that starts with /dir/dir2/ is included under the set rule


### Configurations:

- You can use the internal configuration file through the data_reader, as you please  \
You can add/delete/modify configs through the website, be vary not to delete these system configs (or else, things WILL break):  

 TokenExpire: Sets the amount of time, login tokens are valid for (seconds)  \
 RefreshDataFrequency: Tells the data reader, how often it should refresh its contents  \
 PageDisabledSite: Users get redirected here when a page is disabled  \
 UserDisabledSite: Disabled users get redirected here  

 ### Plugins

- Plugins may have any number and structure of folders
- It MUST have a main python file with the name of the plugin (for Template_plugin, you have to name it Template_plugin.py)
- In the main python file, you may import other local python files, and access your assets using ./
- It has to contain the subroutines for your website, alongside any other subroutines you may want to implement
- Upon startup, the server is going to initialise all plugins, but active reloading is not implemented (too resource heavy), if a  plugin is changed, press "Reload Plugin" on the plugins page
- Plugins are to be placed in the "plugins" folder in a subfolder, holding the name of the plugin
- All actions are logged in /log/PLUGINNAME_log.txt in the webservice's root folde