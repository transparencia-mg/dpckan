from setuptools import setup, find_packages
import codecs
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import package_information

# PREPARE

INSTALL_REQUIRES = [
    "frictionless-ckan-mapper>=1.0.6",
    "python-dotenv>=0.19.1",
    "ckanapi>=4.0.0",
    "frictionless>=4.16.6",
    "click>=8.0.1"
]

if __name__ == '__main__':
  # Setting up
  setup(
      name=package_information.name,
      version=package_information.version,
      author=package_information.author,
      author_email=package_information.email_author,
      description=package_information.description,
      long_description_content_type="text/markdown",
      long_description=open('README.md', encoding='utf-8').read() + '\n\n' + open('CHANGELOG.md', encoding='utf-8').read(),
      url="https://github.com/dados-mg/dpkgckanmg",
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      keywords=['python', 'ckan'],
      classifiers=[
          "Development Status :: 1 - Planning",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 3",
          "Operating System :: Unix",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows",
      ],
      entry_points="""
        [console_scripts]
        dpckan=dpckan.cli:cli
      """
  )
