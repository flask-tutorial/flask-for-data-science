## Example App

This is an example web app written with flask.  Just enough
code to get you started with collecting data, writing it to a database,
and displaying it again in a table or on a map.

share and enjoy!

### 

copy config-sample.py to config.py and edit it 

create the sqlite-database:

    sqlite3 ./database.db < schema.sql

start the webserver locally:

    python flaskfile.py

or, if you are deploying to a real webserver, set up wsgi:

    import sys
    path = '..../flask-for-data-science'
    
    if path not in sys.path:
      sys.path.insert(0, path)
   
    from flaskfile import app as application

