import config

from peewee import SqliteDatabase, PostgresqlDatabase


#db = SqliteDatabase(config.RESOURCES_DIR / 'db' / 'HealthMonitor.db')

# Connect to a Postgres database.
db = PostgresqlDatabase(
    config.POSTGRES_DB, 
    user=config.POSTGRES_USER, 
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_HOST, 
    port=config.POSTGRES_PORT
)
