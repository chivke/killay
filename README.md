# Killay

## Dev Enviroment

- Docker, Docker Compose
- Precommit

### Build local dev enviroment:

```console
docker-compose build
```

### Run migrations

```console
docker-compose run --rm django python manage.py migrate
```

### Upload dump fixture if you have

```console
docker-compose run --rm django python manage.py loaddata [/path/to/file]
```
- Copy media files to /killay/media

### Start dev server (localhost:7000 / 3000)

```console
docker-compose up
```

### Shell

```console
docker-compose run --rm django python manage.py shell
```

### Create superuser

```console
docker-compose run --rm django python manage.py createsuperuser
```

### Dev Browser
- directly with django: `http://localhost:7000/`
- with auto-reload: `http://localhost:3000/`
- Browsersync UI: `http://localhost:3001/`


### Run Tests

```console
docker-compose run --rm django python manage.py createsuperuser
```

### Run Coverage

```console
docker-compose run --rm django python manage.py coverage run -m pytest && coverage report -m
```
