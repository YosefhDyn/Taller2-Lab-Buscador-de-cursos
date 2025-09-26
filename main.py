main

from crawler import go  # Importa la función 'go' desde crawler.py
from search import search  # Importa la función 'search' desde search.py
from compare import compare  # Importa la función 'compare' desde compare.py
import json

if _name_ == "_main_":
    print("Starting the crawler...")  # Verifica si el programa llega hasta aquí
    go(100, "dictionary.json", "output.csv")  # Llamamos al crawler con 100 páginas y archivos de salida

    # Cargar el índice (para las comparaciones y búsqueda)
    index = {}
    with open("dictionary.json", 'r', encoding='utf-8') as file:
        index = json.load(file)

    # Ejemplo de comparación entre dos cursos (puedes obtener los ids de los cursos de output.csv)
    similarity = compare("curso-001", "curso-002", index)
    print(f"Similarity between course-001 and course-002: {similarity}")

    # Ejemplo de búsqueda de cursos por palabras clave
    keywords = ['aeronáutica', 'derecho']
    relevant_courses = search(keywords, index)
    print(f"Most relevant courses: {relevant_courses}")
