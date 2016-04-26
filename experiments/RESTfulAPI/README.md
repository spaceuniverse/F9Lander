______________________________________________

###Additional dependencies

**Flask, flask-restful**

Install:

```bash
$ pip install flask-restful

$ pip install Flask
```

Use `sudo` if needed or read the official installation guides.

______________________________________________

###Command line options and how to run:

Start the server script:

```bash
$ python F9LanderCORE_REST.py
```

Then run in second console:

```bash
$ python F9LanderClient_REST.py
```

You can run game without graphics with text output only (graphics is enabled by default):

```bash
$ python F9LanderCORE_REST.py -d
```

______________________________________________

###API

"http://localhost:5000/0001" - restart

"http://localhost:5000/1000"

"http://localhost:5000/0100"

"http://localhost:5000/0010" - engines

You can send any combinations of engines such as 1110, 1010 etc.

Map (first digit - main engine, second - left engine, third - right engine, fourth - new rocket / restart)

For example (1110) means that all engines are working. (0001) means that you want to get a new rocket and restart.

You can find more information about controls in root `README.md`

______________________________________________

###Information

http://flask.pocoo.org/docs/0.10/quickstart/#

http://flask.pocoo.org/docs/0.10/installation/#installation

https://flask-restful.readthedocs.org/en/0.3.5/quickstart.html

https://flask-restful.readthedocs.org/en/0.3.5/installation.html#installation

______________________________________________

###Help

http://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful

http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

______________________________________________
