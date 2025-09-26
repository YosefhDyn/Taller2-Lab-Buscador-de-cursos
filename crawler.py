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

# Lista de palabras clave no deseadas que queremos excluir del índice
STOPWORDS = {"tipo", "nivel", "facultades", "modalidad", "duración", "acceso", "curso", "universidad", "educación", "estudios", "artes", "salud", "informática"}

# Función para rastrear las páginas
def go(n, dictionary, output):
    visited_urls = set()
    queue = deque(["https://educacionvirtual.javeriana.edu.co/nuestros-programas-nuevo"])  # URL de inicio
    index = {}

    # Configurar Selenium
    chrome_options = Options()
    chrome_options.headless = True  # Ejecutar sin abrir el navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Abrir el archivo CSV correctamente para escribir los cursos
    try:
        with open(output, 'w', newline='', encoding='utf-8') as output_file:
            csv_writer = csv.writer(output_file, delimiter='|')
            csv_writer.writerow(['course_id', 'course_name'])  # Cabecera del archivo CSV con ID y nombre del curso
            print(f"CSV file '{output}' opened successfully.")
    except Exception as e:
        print(f"Error opening CSV file: {e}")
        driver.quit()  # Asegurarse de cerrar el navegador
        return

    course_counter = 1  # Contador para generar IDs únicos para cada curso

    while queue and len(visited_urls) < n:
        url = queue.popleft()
        if url in visited_urls:
            continue
        visited_urls.add(url)
        print(f"Requesting: {url}")

        # Cargar la página con Selenium
        driver.get(url)
        print(f"Page loaded: {url}")
        time.sleep(5)  # Esperar 5 segundos para asegurarse de que la página cargue

        html_content = driver.page_source
        print(f"HTML content received: {html_content[:1000]}...")  # Muestra los primeros 1000 caracteres del HTML para depuración

        soup = BeautifulSoup(html_content, "html.parser")  # Usamos el parser predeterminado de BeautifulSoup

        # Extraer los enlaces de las categorías
        category_links = extract_category_links(soup)
        print(f"Extracted category links: {category_links}")
        if category_links:
            for category_link in category_links:
                if category_link not in visited_urls:
                    queue.append(category_link)  # Agregar los enlaces de categorías a la cola para seguirlos
        else:
            print("No category links found.")

        # Extraer los cursos de la página actual
        courses = extract_courses(soup)
        print(f"Extracted courses: {courses}")  # Verifica que se están extrayendo los cursos
        if courses:
            with open(output, 'a', newline='', encoding='utf-8') as output_file:
                csv_writer = csv.writer(output_file, delimiter='|')
                for course in courses:
                    course_id = f"course-{course_counter}"  # Asigna un ID único para cada curso
                    course_counter += 1  # Incrementa el contador para el siguiente curso
                    # Aquí, guardamos el ID y el nombre del curso en el CSV
                    csv_writer.writerow([course_id, course])
                    print(f"Saving: {course_id} | {course}")  # Muestra lo que se está guardando
                    # También agregamos el curso al índice para generar el diccionario
                    index_course(index, course, course_id)  # Usamos el ID único del curso
        else:
            print("No courses found on this page.")

    # Al finalizar, guardamos el diccionario de palabras clave
    print("Saving dictionary to JSON...")
    generate_dictionary(index, dictionary)  # Guardamos el diccionario como archivo JSON

    print("Index before saving:", index)  # Muestra el índice antes de guardarlo

    # Guardamos el índice de palabras clave en el archivo CSV
    with open(output, 'a', newline='', encoding='utf-8') as output_file:
        save_index(index, output_file)  # Guarda el índice en el archivo CSV

    driver.quit()  # Asegurarse de cerrar el navegador al final

# Función para extraer enlaces de categorías
def extract_category_links(soup):
    links = []
    for div in soup.find_all('div', class_="item2"):  # Usamos la clase 'item2' como vemos en el HTML
        a_tag = div.find('a', href=True)  # Buscamos los enlaces dentro de 'a'
        if a_tag:
            link = a_tag['href']  # Extraemos el href del enlace
            links.append(link)
    print(f"Extracted category links: {links}")  # Imprime los enlaces extraídos
    return links

# Función para extraer cursos
def extract_courses(soup):
    courses = []
    for div in soup.find_all('div', class_="card-body"):  # Ajusta la clase si es diferente
        title_tag = div.find('b', class_="card-title text-primary font-weight-bold")  # Clase actualizada
        if title_tag:
            course_name = title_tag.text.strip()  # Extraemos solo el nombre del curso
            courses.append(course_name)

    print(f"Extracted courses: {courses}")  # Imprime los cursos extraídos
    return courses

# Función para indexar palabras en el índice
def index_course(index, text, course_id):
    words = re.findall(r'\b\w+\b', text.lower())  # Buscar palabras alfanuméricas
    for word in words:
        if word in STOPWORDS or len(word) <= 2:
            continue  # Ignorar palabras de 1 o 2 caracteres
        if word not in index:
            index[word] = []
        if course_id not in index[word]:
            index[word].append(course_id)

# Función para guardar el índice en un archivo CSV
def save_index(index, output_file):
    if index:
        for word, courses in index.items():
            for course_id in courses:
                output_file.write(f"{course_id}|{word}\n")
                print(f"Saving: {course_id}|{word}")
    else:
        print("No data in index to save.")

# Función para guardar el diccionario como un archivo JSON
def generate_dictionary(index, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
        print(f"Dictionary saved to {output_file}")
