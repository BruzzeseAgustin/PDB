from setuptools import setup

setup(
  name = 'scrapdb',
  packages = ['scrapdb'], # same as 'name'
  version = '0.1',
  install_requires=[
        'xmltodict', 
        'beautifulsoup4',
        'numpy',
        'urllib',
        'datetime',
        'pymysql',
        'logging',
        'requests',
        'SQLConnection',
        'linecache',
        'webbrowser',
        'selenium',
        'requests_html'
  ],
  description = 'A Python scrapper for the RCSB Protein Data Bank (PDB) API',
  author = 'Agustin Bruzzese',
  author_email = 'bruzzese.agustin@gmail.com',
  url = 'https://github.com/BruzzeseAgustin/PDB',
  download_url = 'https://github.com/BruzzeseAgustin/PDB', 
  keywords = ['protein','data','api'],
  classifiers = [],
)