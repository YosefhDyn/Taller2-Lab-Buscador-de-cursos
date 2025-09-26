import csv
import psycopg2  

# Conectar a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="courses",  # Cambia el nombre de la base de datos si es necesario
    user="postgres",     # Cambia el usuario de la base de datos
    password="olaQUE248",  # Cambia la contraseña de la base de datos
    host="localhost",     # Cambia si tu servidor de base de datos no está en localhost
    port="5432"           # Puerto por defecto para PostgreSQL
)

cursor = conn.cursor()

# Crear la tabla 'courses' si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
  course_id      VARCHAR(128) PRIMARY KEY,
  course_name    TEXT NOT NULL
);
""")

# Función para cargar los cursos en la base de datos
def load_courses_to_db(input_csv):
    with open(input_csv, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter='|')
        next(csv_reader)  # Saltar la cabecera

        for row in csv_reader:
            course_id = row[0]
            course_name = row[1]

            # Insertar el curso en la tabla 'courses'
            cursor.execute("""
            INSERT INTO courses (course_id, course_name) 
            VALUES (%s, %s)
            ON CONFLICT (course_id) DO NOTHING;  -- Evitar duplicados
            """, (course_id, course_name))

    # Guardar los cambios
    conn.commit()

# Llamar a la función para cargar los cursos
input_csv = 'output.csv'  # Ruta del archivo CSV con los cursos
load_courses_to_db(input_csv)

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()

print("Datos insertados exitosamente en la base de datos.")
