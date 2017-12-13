from flask import Flask, render_template, flash, redirect, url_for, request, session
from subprocess import Popen
from time import gmtime, strftime, sleep

app = Flask(__name__)
prc = None

# globals holding last arguments to worker
last_person = ''
setup_time = ''
interval = '0.1'
density = '8'
redmin = bluemin = greenmin = '0'
redmax = bluemax = greenmax = '250'
keep = '2'

@app.route('/')
def index():
  colour_values = [x for x in range(0,256,10)]
  return render_template(
    'index.html',
    colour_values=colour_values,
    name=last_person,
    setup_time=setup_time,
    interval=interval,
    density=density,
    redmin=redmin,
    redmax=redmax,
    bluemin=bluemin,
    bluemax=bluemax,
    greenmin=greenmin,
    greenmax=greenmax,
    keep=keep
  )

@app.route('/sparkle', methods=['POST'])
def sparkle():
  global prc, last_person, setup_time
  global interval, density, keep, sequence
  global redmin, redmax, greenmin, greenmax, bluemin, bluemax

  if prc:
    prc.terminate()
    sleep(0.1) # let it finish, Pi is slow
    prc = None

  # collect data from the form
  last_person = request.form['person'] if not request.form['person'] == '' else 'Anonymous'
  interval = request.form['interval']
  density = request.form['density']
  redmin = request.form['redmin']
  redmax = request.form['redmax']
  red = '%s,%s' % (redmin, redmax)
  greenmin = request.form['greenmin']
  greenmax = request.form['greenmax']
  green = '%s,%s' % (greenmin, greenmax)
  bluemin = request.form['bluemin']
  bluemax = request.form['bluemax']
  blue = '%s,%s' % (bluemin, bluemax)
  keep = request.form['keep']
  sequence = request.form['sequence']

  # make an args string for the worker
  args = ['./sparklemote.py', '-i', interval, '-d', density, '-r', red, '-g', green, '-b', blue]
  if keep == '1':
    args.append('-k')
  args.append(sequence)
  setup_time = strftime("%I:%M %p", gmtime()).lstrip('0')
  # call worker
  prc = Popen(args)
  sleep(0.1) # let it get started, Pi is slow

  return redirect(url_for('index'))

@app.route('/stop/')
def stop():
  global prc
  if prc:
    prc.terminate()
  return redirect(url_for('index'))
