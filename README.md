# BiciMad

**BiciMad** es un paquete de Python diseñado para analizar datos de uso de bicicletas en Madrid proporcionados por el sistema BiciMAD. Este paquete permite extraer, limpiar y analizar datos históricos de uso de bicicletas eléctricas, facilitando la generación de resúmenes y la consulta de información específica sobre el rendimiento del sistema.

## Características

- Extracción de datos de la web de EMT de Madrid usando la clase `UrlEMT`.
- Limpieza y transformación de los datos de uso de bicicletas con la clase `BiciMad`.
- Generación de resúmenes con información estadística clave, como el total de usos, tiempo total, y la estación más popular.
- Tests automatizados para garantizar la robustez del código.
- Fácil integración en proyectos de análisis y visualización de datos.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Requisitos](#requisitos)
- [Tutorial de Inicio Rápido](#tutorial-de-inicio-rápido)
  - [1. Extracción de Datos](#1-extracción-de-datos)
  - [2. Limpieza y Análisis de Datos](#2-limpieza-y-análisis-de-datos)
- [Ejecución de Tests](#ejecución-de-tests)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Estructura 

bicimad_project/
├── bicimad/
│   ├── __init__.py
│   ├── bicimad.py            # Clase BiciMad para limpieza y análisis de datos
│   └── urlemt.py             # Clase UrlEMT para manejo de enlaces y extracción de CSV
├── tests/
│   ├── __init__.py
│   ├── test_bicimad.py       # Pruebas unitarias para BiciMad
│   └── test_urlemt.py        # Pruebas unitarias para UrlEMT
├── setup.py                  # Script de instalación para el paquete
└── README.md                 # Documentación del proyecto

## Instalación

### Opción 1: Clonar y usar `setup.py`

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/bicimad_project.git
   cd bicimad_project

## Requisitos

Este proyecto requiere Python 3.6 o superior y las siguientes dependencias:

- `pandas>=1.0.0`
- `requests>=2.0.0`

Instala los requisitos con:
```bash
pip install -r requirements.txt

## Tutorial de Inicio Rápido

Este tutorial te guiará paso a paso en el uso de las principales funcionalidades de `BiciMad`.

### 1. Extracción de Datos

La clase `UrlEMT` facilita la obtención de los enlaces de datos de uso de bicicletas desde el sitio web de EMT de Madrid.

1. Importa la clase `UrlEMT` y crea una instancia:
   ```python
   from bicimad.urlemt import UrlEMT

   url_emt = UrlEMT()
