from bicimad.bicimad import (UrlEMT)  # Cambia 'url_emt' si has guardado la clase en otro archivo


def main():
    # Crear la instancia de la clase
    bicimad = UrlEMT()

    # Probar select_valid_urls para obtener y almacenar los enlaces válidos
    print("Probando select_valid_urls...")
    bicimad.select_valid_urls()

    # Probar get_url para obtener el enlace de un mes y año específico
    print("\nProbando get_url para junio de 2021...")
    try:
        url = bicimad.get_url(6, 21)  # Cambia los valores para probar con otros meses y años
        print("URL encontrada:", url)
    except ValueError as e:
        print("Error:", e)

    # Probar get_csv para descargar y leer el archivo CSV de un mes y año específico
    print("\nProbando get_csv para junio de 2021...")
    try:
        csv_file = bicimad.get_csv(6, 21)  # Cambia los valores para probar con otros meses y años
        print("Contenido del CSV:")
        print(csv_file.read())
    except (ValueError, ConnectionError) as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
