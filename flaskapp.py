from flask import Flask, render_template, flash, redirect, url_for, request, session
from subprocess import Popen

app = Flask(__name__)
app.secret_key = 'ed234d80111dc32b7824f25ef72ee53e'
prc = None
last_person = ''

@app.route('/')
def index():
  session['person'] = last_person
  return render_template('index.html')

@app.route('/sparkle', methods=['POST'])
def sparkle():
  global prc
  global last_person
  session['person'] = request.form['person']
  last_person = session['person']

  status = 'called'
  if prc:
    prc.terminate()
    status = '%s and stopped' % status
  interval = request.form['interval']
  density = request.form['density']
  colourmin = request.form['colourmin']
  colourmax = request.form['colourmax']
  blockcolour = request.form['blockcolour']
  args = ['./sparklemote.py', '-i', interval, '-d', density, '-c', colourmin, '-m', colourmax]
  args.append('sparkle')
  if blockcolour == 'yes':
    args.append('-b')
  print(args)
  prc = Popen(args)
  status = '%s and started.' % status
  flash(status)
  return redirect(url_for('index'))

@app.route('/stop/')
def stop():
  global prc
  status = 'Stopping'
  if prc:
    prc.terminate()
    status = '%s and stopped' % status
  else:
    status = '%s but nothing to stop' % status
  status = '%s.' % status
  flash(status)
  return redirect(url_for('index'))