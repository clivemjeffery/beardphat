from flask import Flask, render_template, flash, redirect, url_for
from subprocess import Popen

app = Flask(__name__)
app.secret_key = 'ed234d80111dc32b7824f25ef72ee53e'
prc = None

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/sparkle/')
@app.route('/sparkle/<int:mincolour>')
def sparkle(mincolour=0):
  global prc
  status = 'called'
  if prc:
    prc.terminate()
    status = '%s and stopped' % status
  args = ['./sparklemote.py',
    'sparkle',
    '-i','0.1',
    '-c', str(mincolour),
    '-m','255']
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