# This is a website hosting my custom server control software
## Made for python 3.11
## Rules for changing Site Permissions:
### Set access_level

- -1 = no one may access
- 0 = only accessible by certain users and groups
- 1 = anyone with the set permission level or one above it may access (set with perm_level column, permission level of a user is determined by their highest ranking group or role, except if they have the a role/group with the permission level -1, in which case all endpoints are denied)
- not in the list = accessible to anyone


### Fill out group/rule/user ids

- if -1 is present in user_access_role and access_level is 0 then the URL must end in an id (eg. /user/1)
in this case the given id may be provided access too

/dir/dir2/* means anything that starts with /dir/dir2/ is included under the set rule


### Configurations

- You can use the internal configuration file through the data_reader, as you please  \
You can add/delete/modify configs through the website, be vary not to delete these system configs (or else, things WILL break):  

 TokenExpire: Sets the amount of time, login tokens are valid for (seconds)  \
 RefreshDataFrequency: Tells the data reader, how often it should refresh its contents  \
 PageDisabledSite: Users get redirected here when a page is disabled  \
 UserDisabledSite: Disabled users get redirected here  \
 LoggingEnabled: 1 or 0; tells the program whether to log or not \
 LogFolder: Tells the program where to write logs \
 LogPrint: 1 or 0; Whether the logging program prints to the console or not \
 PluginDefaultState: 1 or 0; when a plugin is first imported its going to either become Enabled if this value is 1 or disabled if its 0 \
 NonExistentUserLogs: 1 or 0; Whether the program makes login logs on non-existent usernames (If this is off and someone has access to logs they may be able to enumerate valid usernames) \
 APIEnabled: 1 or 0; whether the API is enabled or not

 ### Plugins

- Plugins may have any number and structure of folders and files
- The program still runs in ./ compared to main.py so if you want to use something from the plugin's folder use the correct subfolder (set in PluginData.path)
- It MUST have an init python file named \__plugin_init__.py
- In the main python file, you may import other local python files, and access your assets, but u may have to use /plugins/PLUGINNAME/...
- It has to contain the subroutines for your endpoint
- Upon startup, the server is going to initialise all plugins, but active reloading is not implemented (too resource heavy), if a  plugin is changed, press "Reload Plugin" on the plugins page
- Plugins are to be placed in the "plugins" folder in a subfolder, holding the name of the plugin
- All actions are logged in /log/PLUGINNAME_log.txt in the webservice's root folder
- You may set configs for the plugins. You must create a file called "\__plugin_configs__.json" in the plugin's root folder and write the config as  {"key":value, "key2":value2} (standard JSON format)
- You can change the configs trough the plugin manager page
- You can access the main site's data through the data reader
- Uploading folders through a webpage is sadly not possible, therefore they must be uploaded through SFTP or some other protocol (setting up a local test environment is also advised for development)


### Logging

- Logging is done with the "LLogger" module, import it into any program to log
- Logging may be turned on/off using the config
- The module logs into the folder specified in the config folder
- When logging, you must specify a category, a severity, and the text of the error
- In order to test that logging works, press "Test logging" on the logs page
- In order not to break stuff, backslashes are removed, so the formatting wont cause problems
- Usage:
    ```
        from LLogger import *
        CreateLog(category, severity, text)
    ```
- Parameters:
        category: written as "cat1/cat2/cat3/service" ==> File is going to be created at "./$LOG_FOLDER$/cat1/cat2/cat3/service/yyyy-mm-dd.log"
        severity: 0-2 --> 0: [MESSAGE]    1: [WARNING]      2: [ERROR]
        text: what's going to be written in the logs

### Auto Disable
- Used to disable users, after a certain amout of incorrect login tries
- Set to <=0 to disable
- A role called "Disabled" must exist for this to function, and its perm level must be set to -1 (or it wont actually disable the users)
- set AutoDisable config to the number of tries, after which the program should disable a profile
- __*WARNING*__: ONLY do this if ssh or other contact to the machine is possible, otherwise its possible to lock all accounts, by spamming login requests

### Auto Update
- SystemUpdateFreq MUST be present in the config, and must be an integer, otherwise the Auto Update system just won't work
- SystemUpdateFreq represents the number of minutes between each check to the selected git repo
- if SystemUpdateFreq is less than 1, the Auto update system will turn off

- SystemUpdateRepo is the link to the correct branch you want to update from. 
- If "/tree/REPO" is not specified the system will default to "/tree/stable" (e.g. https://github.com/Levvi07/Webmanager/tree/stable)

- The Auto Update system only updates system files, and the format of csv files (if changed). This means that folders like `./plugins` and `./logs` will remain untouched.
- Should there be a change in the csv files, you will have to download the current csv data file, fill any new columns with data, and upload a csv file of the correct format, OR press the "Leave Empty" button, to leave all new columns empty. If columns are deleted you will have to confirm the changes, except if "AutoConfirmDeletes" is set to 1 in the configs.
