import re

def construir_indice(cursos):
    """construye el indice de cursos a partir de las descripciones :0"""
    indice = {}
    
    for id_curso, descripcion in cursos.items():
        palabras = re.findall(r'\b\w+\b', descripcion.lower())  # extrae las palabras
        for palabra in palabras:
            if palabra not in indice:
                indice[palabra] = []
            indice[palabra].append(id_curso)
    
    return indice
