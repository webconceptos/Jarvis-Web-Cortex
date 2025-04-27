import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import time


# Cargar variables de entorno
load_dotenv()

# Esperar unos segundos para que Postgres termine de levantar
time.sleep(10)

# Base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://jarvis:securepass@postgres:5432/jarvisdb")

# Conexión inicial
def create_users_table():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        hashed_password TEXT NOT NULL,
        disabled BOOLEAN DEFAULT FALSE
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Ejecutar creación
if __name__ == "__main__":

    create_users_table()
    print("✅ Tabla 'users' verificada o creada correctamente.")
