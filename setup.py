from setuptools import setup, find_packages

setup(
    name="amazon-scraping",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "pandas",
        "pytest",
    ],
    author="Theturus GOUDAN",
    author_email="theturus21@gmail.com",
    description="Un outil pour extraire les avis Amazon à partir de fichiers HTML",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/theturus/amazon-scraping",
)