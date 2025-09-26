def search(keywords, index):
    relevance = {}  # Diccionario para almacenar la relevancia de cada curso

    for word in keywords:
        word = word.lower()
        if word in index:
            for course_id in index[word]:
                if course_id not in relevance:
                    relevance[course_id] = 0
                relevance[course_id] += 1  # Incrementar relevancia por coincidencia

    # Ordenar los cursos por relevancia
    sorted_relevance = sorted(relevance.items(), key=lambda x: x[1], reverse=True)
    return [course_id for course_id, score in sorted_relevance]
