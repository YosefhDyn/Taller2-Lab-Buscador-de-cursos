import requests
from bs4 import BeautifulSoup
from collections import deque
import re
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# lista de palabras clave no deseadas que queremos excluir del indice :|
STOPWORDS = {"tipo", "nivel", "facultades", "modalidad", "duracion", "acceso", "curso", "universidad", "educacion", "estudios", "artes", "salud", "informatica"}

# funcion para rastrear las paginas :0
def go(n, dictionary, output):
    visited_urls = set()
    queue = deque(["https://educacionvirtual.javeriana.edu.co/nuestros-programas-nuevo"])  # url de inicio
    index = {}

    # configurar selenium
    chrome_options = Options()
    chrome_options.headless = True  # ejecutar sin abrir el navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # abrir el archivo csv correctamente para escribir los cursos :)
    try:
        with open(output, 'w', newline='', encoding='utf-8') as output_file:
            csv_writer = csv.writer(output_file, delimiter='|')
            csv_writer.writerow(['course_id', 'course_name'])  # cabecera del archivo csv con id y nombre del curso
            print(f"csv file '{output}' opened successfully.")
    except Exception as e:
        print(f"error abriendo el archivo csv: {e}")
        driver.quit()  # asegurarse de cerrar el navegador
        return

    course_counter = 1  # contador para generar ids unicos para cada curso

    while queue and len(visited_urls) < n:
        url = queue.popleft()
        if url in visited_urls:
            continue
        visited_urls.add(url)
        print(f"requesting: {url}")

        # cargar la pagina con selenium
        driver.get(url)
        print(f"page loaded: {url}")
        time.sleep(5)  # esperar 5 segundos para asegurarse de que la pagina cargue

        html_content = driver.page_source
        print(f"html content received: {html_content[:1000]}...")  # muestra los primeros 1000 caracteres del html para depuracion

        soup = BeautifulSoup(html_content, "html.parser")  # usamos el parser predeterminado de BeautifulSoup

        # extraer los enlaces de las categorias
        category_links = extract_category_links(soup)
        print(f"extracted category links: {category_links}")
        if category_links:
            for category_link in category_links:
                if category_link not in visited_urls:
                    queue.append(category_link)  # agregar los enlaces de categorias a la cola para seguirlos
        else:
            print("no category links found.")

        # extraer los cursos de la pagina actual
        courses = extract_courses(soup)
        print(f"extracted courses: {courses}")  # verifica que se estan extrayendo los cursos
        if courses:
            with open(output, 'a', newline='', encoding='utf-8') as output_file:
                csv_writer = csv.writer(output_file, delimiter='|')
                for course in courses:
                    course_id = f"course-{course_counter}"  # asigna un id unico para cada curso
                    course_counter += 1  # incrementa el contador para el siguiente curso
                    # aqui, guardamos el id y el nombre del curso en el csv
                    csv_writer.writerow([course_id, course])
                    print(f"saving: {course_id} | {course}")  # muestra lo que se esta guardando
                    # tambien agregamos el curso al indice para generar el diccionario
                    index_course(index, course, course_id)  # usamos el id unico del curso
        else:
            print("no courses found on this page.")

    # al finalizar, guardamos el diccionario de palabras clave
    print("saving dictionary to json...")
    generate_dictionary(index, dictionary)  # guardamos el diccionario como archivo json

    print("index before saving:", index)  # muestra el indice antes de guardarlo

    # guardamos el indice de palabras clave en el archivo csv :|
    with open(output, 'a', newline='', encoding='utf-8') as output_file:
        save_index(index, output_file)  # guarda el indice en el archivo csv

    driver.quit()  # asegurarse de cerrar el navegador al final :)

# funcion para extraer enlaces de categorias :|
def extract_category_links(soup):
    links = []
    for div in soup.find_all('div', class_="item2"):  # usamos la clase 'item2' como vemos en el html
        a_tag = div.find('a', href=True)  # buscamos los enlaces dentro de 'a'
        if a_tag:
            link = a_tag['href']  # extraemos el href del enlace
            links.append(link)
    print(f"extracted category links: {links}")  # imprime los enlaces extraidos
    return links

# funcion para extraer cursos :0
def extract_courses(soup):
    courses = []
    for div in soup.find_all('div', class_="card-body"):  # ajusta la clase si es diferente
        title_tag = div.find('b', class_="card-title text-primary font-weight-bold")  # clase actualizada
        if title_tag:
            course_name = title_tag.text.strip()  # extraemos solo el nombre del curso
            courses.append(course_name)

    print(f"extracted courses: {courses}")  # imprime los cursos extraidos
    return courses

# funcion para indexar palabras en el indice :)
def index_course(index, text, course_id):
    words = re.findall(r'\b\w+\b', text.lower())  # buscar palabras alfanumericas
    for word in words:
        if word in STOPWORDS or len(word) <= 2:
            continue  # ignorar palabras de 1 o 2 caracteres
        if word not in index:
            index[word] = []
        if course_id not in index[word]:
            index[word].append(course_id)

# funcion para guardar el indice en un archivo csv :|
def save_index(index, output_file):
    if index:
        for word, courses in index.items():
            for course_id in courses:
                output_file.write(f"{course_id}|{word}\n")
                print(f"saving: {course_id}|{word}")
    else:
        print("no data in index to save.")

# funcion para guardar el diccionario como un archivo json :)
def generate_dictionary(index, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
        print(f"dictionary saved to {output_file}")
