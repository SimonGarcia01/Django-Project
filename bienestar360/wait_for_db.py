import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_postgres(
    db_name="bienestar",
    db_user="bienestaruser",
    db_pass="bienestarpass",
    db_host="db",
    db_port="5432",
):
    while True:
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_pass,
                host=db_host,
                port=db_port,
            )
            conn.close()
            print("✅ Postgres available")
            break
        except OperationalError:
            print("⏳ Waiting for Postgres...")
            time.sleep(1)


# Only run automatically when executed directly, NOT when imported
if __name__ == "__main__":
    wait_for_postgres()