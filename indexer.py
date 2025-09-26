import re

# Función para indexar palabras clave a cursos
def index_course(index, text, course_id):
    words = re.findall(r'\b\w+\b', text.lower())  # Buscar palabras alfanuméricas
    for word in words:
        if len(word) <= 2:  # Ignorar palabras muy cortas
            continue
        if word not in index:
            index[word] = []
        if course_id not in index[word]:
            index[word].append(course_id)
