from crawler import go  # importa la funcion 'go' desde crawler.py :|
from search import search  # importa la funcion 'search' desde search.py :)
from compare import compare  # importa la funcion 'compare' desde compare.py :0
import json

if __name__ == "__main__":  # verifica si el programa llega hasta aqui :)
    print("starting the crawler...")  # verifica si el programa llega hasta aqui
    go(100, "dictionary.json", "output.csv")  # llamamos al crawler con 100 paginas y archivos de salida :)

    # cargar el indice (para las comparaciones y busqueda) :|
    index = {}
    with open("dictionary.json", 'r', encoding='utf-8') as file:
        index = json.load(file)

    # ejemplo de comparacion entre dos cursos (puedes obtener los ids de los cursos de output.csv) :0
    similarity = compare("curso-001", "curso-002", index)
    print(f"similarity between course-001 and course-002: {similarity}")

    # ejemplo de busqueda de cursos por palabras clave :(
    keywords = ['aeronautica', 'derecho']
    relevant_courses = search(keywords, index)
    print(f"most relevant courses: {relevant_courses}")
