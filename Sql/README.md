# Taller2-Lab-Buscador-de-cursos
README - Laboratorio 2: Motor de Búsqueda de Cursos

Hecho por: Julio Useche Llanos y Yosefh Steven Peña Rodriguez

Descripción del Taller
Este taller tiene como objetivo desarrollar un motor de búsqueda de cursos que se conecta al catálogo universitario de la Universidad Javeriana a través de un rastreador web. El motor permite rastrear páginas, construir un índice de cursos y realizar búsquedas por relevancia de acuerdo con los intereses del usuario. Se incluyen funciones para comparar cursos y retornar aquellos que mejor se ajusten a los intereses de los usuarios.

Estructura del Taller
El taller se compone de varios archivos esenciales para su funcionamiento:

1. crawler.py: Contiene el código para el rastreo de las páginas del catálogo, extrayendo los títulos, descripciones y enlaces de los cursos. Construye un índice de palabras clave a partir del contenido de las páginas.

2. search.py: Implementa la función de búsqueda de cursos basada en un listado de palabras clave de interés. Devuelve los cursos más relevantes según los intereses proporcionados.

3. compare.py: Contiene la función para calcular la similitud entre dos cursos, utilizando una métrica de similitud basada en las palabras clave asociadas a los cursos.

4. output.csv: Archivo de salida generado por el rastreador, que contiene el índice de palabras clave relacionadas con cada curso.

5. index.sql: Base de datos con la salida del rastreo, estructurada para facilitar consultas posteriores.

Requerimientos

Python 3.x: Asegúrate de tener instalada la versión correcta de Python.
Bibliotecas de Python necesarias:

1. requests
2. BeautifulSoup4
3. html5lib
4. pandas (para el manejo de datos en el archivo CSV)
5. selenium
6. archivos json

Puedes instalar estas bibliotecas usando el siguiente comando:

"pip install requests beautifulsoup4 html5lib pandas"

Instrucciones de Uso
1. Rastrear el catálogo de cursos

Para iniciar el rastreo del catálogo de cursos, ejecuta el siguiente comando en tu terminal:
"python crawler.py"

Este comando iniciará el rastreo a partir de la URL especificada en el código (https://educacionvirtual.javeriana.edu.co/nuestros-programas-nuevo). Se detendrá cuando haya visitado el número máximo de páginas especificado en el código.

2. Búsqueda de cursos
Para realizar una búsqueda de cursos relacionados con ciertos intereses, ejecuta el siguiente comando:
"python search.py "palabra_clave1 palabra_clave2 palabra_clave3""

Este comando retornará los cursos más relevantes según las palabras clave ingresadas.

3. Comparar cursos
Para comparar dos cursos y obtener su medida de similitud, ejecuta el siguiente comando:
"python compare.py curso1_id curso2_id"

Esto te proporcionará un valor de similitud entre 0 y 1, donde 1 significa cursos idénticos y 0 significa cursos completamente diferentes.

Conclusiones

Este taller proporciona una herramienta útil para analizar y buscar cursos en el catálogo de una universidad, permitiendo comparar cursos basados en similitudes y facilitar la búsqueda por intereses específicos. A través de la implementación de un rastreador web, se logró indexar el contenido del catálogo, mientras que las funciones de comparación y búsqueda permiten personalizar la experiencia del usuario.
