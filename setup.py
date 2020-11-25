from setuptools import setup, find_packages
from io import open
from os import path

import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup (
  name = 'python-prolog-shell',
  version = '1.4.0',
  author="Nguyen Hoang Nam",
  author_email="nguyenhoangnam.dev@gmail.com"
  description = 'Python Prolog shel is a Python CLI for runing prolog query in terminal.',
  long_description=README,
  long_description_content_type="text/markdown",
  packages = find_packages(), # list of all packages
  # install_requires = install_requires,
  python_requires='>=3', # any python greater than 3
  entry_points='''
          [console_scripts]
          pyrolog=pyrolog.__main__:main
      ''',
  
  keyword="cli, prolog, shell, terminal, interpreter",
  license='MIT',
  url='https://github.com/Nguyen-Hoang-Nam/python-prolog-shell',
  # download_url='https://github.com/CITGuru/cver/archive/1.0.0.tar.gz',
  # dependency_links=dependency_links,
  classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ]
)

# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
# with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
#     all_reqs = f.read().split('\n')

# install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
#   not x.startswith('#')) and (not x.startswith('-'))]
# dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]