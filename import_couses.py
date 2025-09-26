import csv
import psycopg2  

conn = psycopg2.connect(
    dbname="courses",  
    user="postgres",     
    password="olaQUE248",  
    host="localhost",     
    port="5432"           
)

cursor = conn.cursor()

# crear la tabla 'courses' si no existe :)
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
  course_id      VARCHAR(128) PRIMARY KEY,
  course_name    TEXT NOT NULL
);
""")

# funcion para cargar los cursos en la base de datos :|
def load_courses_to_db(input_csv):
    with open(input_csv, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter='|')
        next(csv_reader)  # saltar la cabecera

        for row in csv_reader:
            course_id = row[0]
            course_name = row[1]

            # insertar el curso en la tabla 'courses' :0
            cursor.execute("""
            INSERT INTO courses (course_id, course_name) 
            VALUES (%s, %s)
            ON CONFLICT (course_id) DO NOTHING;  -- evitar duplicados :/
            """, (course_id, course_name))

    # guardar los cambios :)
    conn.commit()

# llamar a la funcion para cargar los cursos :(
input_csv = 'output.csv'  # ruta del archivo csv con los cursos
load_courses_to_db(input_csv)

# cerrar la conexion a la base de datos :|
cursor.close()
conn.close()

print("datos insertados exitosamente en la base de datos.")
