import re

# funcion para indexar palabras clave a cursos :|
def index_course(index, text, course_id):
    words = re.findall(r'\b\w+\b', text.lower())  # buscar palabras alfanumericas :)
    for word in words:
        if len(word) <= 2:  # ignorar palabras muy cortas :/
            continue
        if word not in index:
            index[word] = []
        if course_id not in index[word]:
            index[word].append(course_id)  # agregar el curso al indice :)
