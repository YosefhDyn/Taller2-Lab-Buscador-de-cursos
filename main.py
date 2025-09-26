from crawler import go  # Importa la función go desde crawler.py

if __name__ == "__main__":
    print("Starting the crawler...")  # Verifica si el programa llega hasta aquí
    go(100, "dictionary.json", "output.csv")  # Llamamos al crawler con 100 páginas y archivos de salida

    print("Crawler finished successfully.")
