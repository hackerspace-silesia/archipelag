# archipelag 

## What is it?

An application for NGOs to extend events scope using social media.

First commits application was developed on hackathon HACKSILESIA 2017.

#### How to build?

```bash
docker-compose up --build
```

#### Add superuser?

```bash
docker-compose run --rm backend python manage.py createsuperuser
```

#### copy .env file

```bash
cp .env_example .env
```

### How run tests?

```bash
docker-compose run --rm backend python -m pytest
```
