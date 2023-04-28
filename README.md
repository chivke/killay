# Killay

## Dev Enviroment

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
