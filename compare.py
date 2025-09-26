import math

# Función para calcular la similitud entre dos cursos
def compare(course1, course2, index):
    # Construir el vector de palabras para cada curso
    course1_words = set(index.get(course1, []))
    course2_words = set(index.get(course2, []))

    # Calcular la intersección y las longitudes
    intersection = course1_words.intersection(course2_words)
    norm1 = math.sqrt(len(course1_words))
    norm2 = math.sqrt(len(course2_words))

    # Si alguno de los cursos tiene un conjunto vacío, la similitud es 0
    if norm1 == 0 or norm2 == 0:
        return 0

    return len(intersection) / (norm1 * norm2)  # Similitud de coseno
