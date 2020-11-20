Cars REST API

# Cars REST Api for Netguru

Simple REST API for recruitment proces.

Try this app online on Heroku, just click [here](https://cars-api-bartlomiej-stoklosa.herokuapp.com/)

### Used Technologies:

```
$ Python 3.8.5
$ Django
$ PostgreSQL
$ Docker & Docker Compose
$ Pytest
$ Heroku
$ Bootstrap
```

### Installing

It is best to use the python `virtualenv` tool to build locally:

```sh
$ mkdir app && cd app
$ virtualenv -p python3 venv
$ git clone git@github.com:BartekStok/netguru-home-assignment.git
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python manage.py runserver
```

Then visit `http://localhost:8000` to view the app.

### Using docker-compose

In root directory
```sh
$ docker-compose build
$ docker-compose up
$ docker-compose exec web python manage.py collectstatic
```


### Tests

Project endpoints are tested, in root directory run: 
```sh
$ pytest
```


## License

This project is licensed under the MIT License 

- Copyright 2020 © Bartłomiej Stokłosa
