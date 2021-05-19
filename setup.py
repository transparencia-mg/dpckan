from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1.9010'
DESCRIPTION = 'Funções para gestão de pacotes de dados no portal dados.mg.gov.br'

# Setting up
setup(
    name="dpkgckanmg",
    version=VERSION,
    author="Gabriel Braico Dornas",
    author_email="gabrielbdornas@cge.mg.gov.br",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    url="",
    packages=find_packages(),
    install_requires=["certifi==2020.12.5",
                      "chardet==4.0.0",
                      "frictionless-ckan-mapper==1.0.6",
                      "idna==2.10",
                      "pip==20.2.3",
                      "requests==2.25.1",
                      "setuptools==49.2.1",
                      "six==1.15.0",
                      "urllib3==1.26.3"],
    keywords=['python', 'ckan'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
