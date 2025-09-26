import math

# funcion para calcular la similitud entre dos cursos :|
def compare(course1, course2, index):
    # construir el vector de palabras para cada curso :)
    course1_words = set(index.get(course1, []))
    course2_words = set(index.get(course2, []))

    # calcular la interseccion y las longitudes :0
    intersection = course1_words.intersection(course2_words)
    norm1 = math.sqrt(len(course1_words))
    norm2 = math.sqrt(len(course2_words))

    # si alguno de los cursos tiene un conjunto vacio, la similitud es 0 :(
    if norm1 == 0 or norm2 == 0:
        return 0

    return len(intersection) / (norm1 * norm2)  # similitud de coseno :)
