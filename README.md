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
$ git clone git@github.com:BartekStok/netguru-home-assignment.git
$ cd netguru-home-assignment
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ create database in postgresql
$ rename .env.example to .env 
$ generate secret key using 
    python3 manage.py shell
    from django.core.management.utils import get_random_secret_key
    get_random_secret_key()
$ copy generated key and paste it to .env
$ fill all missing data regarding database
$ python3 manage.py migrate
$ python manage.py runserver
```

Then visit `http://localhost:8000` to view the app.

### Using docker-compose

In root directory
```sh
$ docker-compose build
$ docker-compose up
$ docker-compose exec web python manage.py collectstatic
$ restart docker-compose
```


### Tests

Project endpoints are tested, in root directory run: 
```sh
$ pytest
```


### API - instruction to endpoints

| Method    | URI                      | Params  | 
|-----------|--------------------------|---------|
| GET       | api/cars                 | -       | 
| POST      | api/cars                 | car_make, model_name  |
| POST      | api/rate                 |  car_make, model_name, rating (1-5) |
| GET       | api/popular              | -       | 
- When sending POST on api/cars, car_make could be partial and is case insensitive,
model_name must match exactly, starting with big letter.
- When sending POST to api/rate -> car_make and model_name must be exactly the
same as in local Database (upper or lower case sensitive).

## License

This project is licensed under the MIT License 

- Copyright 2020 © Bartłomiej Stokłosa
