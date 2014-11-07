# ====================================================================================
# Example Flask Web App for Data Scientist
# ====================================================================================
# originially from https://github.com/flask-tutorial/flask-for-data-science

# all the imports
import sqlite3, urllib, json, os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

# this will read in variables from config.py
app.config.from_object("config")


# ====================================================================================
# setup and teardown for each HTTP request
# ====================================================================================
# the @ sign here means that app.before_request is a "decorator" for the function 
# defined in the next line. http://legacy.python.org/dev/peps/pep-0318/#current-syntax
# but you don't have to understand that to use it
#
# in a flask app, putting @app.before_request before a function means
# that this function will be called before a request is routed, and app.teardown_request
# is called after everything is finished.  
# So this is a good place to connect/disconnect to the database
@app.before_request
def before_request():
  g.dir = os.path.dirname(os.path.abspath(__file__))
  g.db  = sqlite3.connect(g.dir + '/' + app.config['DATABASE'])

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

# ====================================================================================
# routes - these map URLs to your python functions
# ====================================================================================
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    abort(401)
  flash('New entry was successfully posted')
  return redirect(url_for('table'))

@app.route('/form', methods=['GET', 'POST'])
def form():
  errors = []
  if request.method == 'POST':
    title = request.form.get('title')
    if len(title) < 3:
      errors.append( 'Please choose a title (at least 3 letters long)' )

    text = request.form.get('text')
    if len(text) < 10:
      errors.append( 'please write the text (at least 10 letters long)' )

    mood = int( request.form.get('mood') )
    if not mood in [1,2,3,4,5]:
      errors.append( 'please choose a mood' )

    if len(errors) == 0:
      g.db.execute('insert into entries (title, text, mood, lat, long) values (?, ?, ?, ?, ?)', 
                   [title, text, mood, request.form.get('lat'), request.form.get('long')])
      g.db.commit()
      flash('Your entry "' + text + '" was saved to the database')
      return redirect( url_for('index') )
  return render_template('form.html', error=", ".join(errors))

@app.route('/table')
def table():
  cur = g.db.execute('select title, text, mood, lat, long from entries order by id desc')
  entries = cur.fetchall()
  return render_template('table.html', entries=entries)

@app.route('/graph')
def graph():
  return render_template('graph.html')

@app.route('/map')
def map():
  cur = g.db.execute('select title, text, mood, lat, long from entries order by id desc')
  entries = cur.fetchall()
  return render_template('map.html', entries=entries)

@app.route('/map_api')
def map_api():
  busline = request.args.get('busline')
  if not busline in ['B26', 'B54', 'B61', 'B69']:
    busline = 'B26'
  url = 'http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s' % (app.config['MTA_KEY'], busline)
  json_data = urllib.urlopen(url).read()
  bus_data = json.loads( json_data )['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]
  entries = []
  if( not 'ErrorCondition' in bus_data.keys() ):
    bus_data = bus_data['VehicleActivity']
    for bus in bus_data:
      location = bus['MonitoredVehicleJourney']['VehicleLocation'] 
      entries.append( location )
    app.logger.info('Found %d busses on line %s' % (len(entries), busline))
  return render_template('map_api.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      session['username'] = request.form['username']
      flash('You were logged in as ' + session['username'])
      return redirect( url_for('index') )
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('index'))

# ====================================================================================
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

# ====================================================================================
if __name__ == '__main__':
  app.run()
# ====================================================================================
