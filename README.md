# beardphat

Mote phat code to sparkle my beard.

I'm attempting to use a [Flask](http://flask.pocoo.org/) to make a web based controller for the beard.

This was useful information from the Flask introduction.

> Once you have virtualenv installed, just fire up a shell and create your own environment. I usually create a project folder and a venv folder within:

````
$ mkdir myproject
$ cd myproject
$ virtualenv venv
New python executable in venv/bin/python
Installing setuptools, pip............done.
````
> Now, whenever you want to work on a project, you only have to activate the corresponding environment. On OS X and Linux, do the following:

````
$ . venv/bin/activate
````

> If you are a Windows user, the following command is for you:

````
$ venv\Scripts\activate
````

> Either way, you should now be using your virtualenv (notice how the prompt of your shell has changed to show the active environment). When you want to go back to the real world, use the following command:

````
$ deactivate
````

After activating the virtual environment, I can run the flask app using something like this.

````
$ export FLASK_APP=flaskapp.py
$ export FLASK_DEBUG=1            -- if wanted
$ flask run
````

I am hoping that I can call the motephat controller from the web interface using the Popen object, stop and restart it using the object's PID. This seems to work on macOS using Python3 and `./sparklemote.py`.

Next steps:

1. Port to a motephat version and try on the Pi, installing flask and maybe virtualenv along the way.
2. Design the API so that it provides a good interface to the sparkle sequence and is general enough for other sequences.
3. Style it.
