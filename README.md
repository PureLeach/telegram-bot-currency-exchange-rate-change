# Telegram bot for notifications of changes in exchange rate quotes

## Problem statement:

**It is necessary to develop a bot that has the following functions:**

1. Display the exchange rates for which the user is subscribed
2. Ability to subscribe and unsubscribe from exchange rates
3. Add a notification when the set value of the currency exchange rate is reached
4. Send a push notification to the user when the set value is reached
5. Delete notifications

## Bot commands:

- `/start` — greeting message
- `/help` — reference
- `/current` — show the current exchange rate
- `/subscribe` — subscribe to the exchange rate
- `/unsubscribe` — unsubscribe from the exchange rate
- `/list_notification` — display a list of notifications
- `/add_notification` — add a notification
- `/remove_notification` — remove notification
- `/remove_all_notification` — remove all notification
- `/cancel` — cancel current action

## Quick Start

1. Copy the settings file and change them

```
cp example.env .env
```

2. Use docker compose to build an image

```
docker-compose build
```

3. Run docker compose up to start the application

```
docker-compose up
```

## Access to PgAdmin:

* **URL:** `http://localhost:5050`
* **Username:** admin@admin.com (as a default)
* **Password:** admin (as a default)

## Add a new server in PgAdmin:

* **Host name/address** `postgres`
* **Port** `5432`
* **Username** as `POSTGRES_USER`, by default: `postgres_user`
* **Password** as `POSTGRES_PASSWORD`, by default `1234`

## Migrations

* Initialization of alembic: `alembic init -t async bot/migrations`
* Create a new migration: `alembic revision --autogenerate -m "migration name"`
* Get information about the current migration: `alembic current`
* Apply migration: `alembic upgrade head`
* Roll back migration: `alembic downgrade -1`
* Roll back migrations to the very beginning: `alembic downgrade base`
