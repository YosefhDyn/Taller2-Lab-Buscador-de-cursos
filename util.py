import requests
from urllib.parse import urljoin

def get_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        print(f"Trying to request: {url}")  # Muestra que está intentando hacer la solicitud
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta tiene un error HTTP
        print(f"Request successful: {url}")  # Muestra si la solicitud fue exitosa
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {url}: {e}")  # Muestra el error si la solicitud falla
        return None


def read_request(request):
    return request.text


def get_request_url(request):
    return request.url


def is_url_ok_to_follow(url, domain):
    if not url.startswith("http"):
        return False
    if domain not in url:
        return False
    if "@" in url or "mailto:" in url:
        return False
    if not url.endswith(".html"):
        return False
    return True


def convert_if_relative_url(base_url, url):
    return urljoin(base_url, url)


def remove_fragment(url):
    return url.split("#")[0]
