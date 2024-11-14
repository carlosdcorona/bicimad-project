from setuptools import setup, find_packages

setup(
    name="bicimad",
    version="1.0.0",
    description="Paquete para análisis de datos de BiciMad",
    author="Carlos Corona",
    author_email="ccoron01@ucm.es",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "requests>=2.0.0",
    ],
    python_requires=">=3.6",
)