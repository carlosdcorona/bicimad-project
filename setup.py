from setuptools import setup, find_packages

setup(
    name="bicimad",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
    ],
    author="Carlos Corona",
    description="Paquete para análisis de datos de BiciMad",
)
