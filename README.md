<h1> This is a website hosting my custom server control software </h1>
<h2>Changing site_perms.csv manually is not advised, but if u must, do it accordingly:</h2>
<h3> perm levels </h3>
    - -1 = no one may access
    - 0 = only accessible by certain users and groups
    - 1 = anyone with the set permission level or one above it may access (set with perm_level column, permission level of a user is determined by their highest ranking group or role)
    - not in the list = accessible to anyone
    - if -1 is present in user_access_role then the URL must end in an id (eg. /user/1)
    in this case the given id may be provided access too

    /dir/dir2/* means anything that starts with /dir/dir2/ is included under the set rule