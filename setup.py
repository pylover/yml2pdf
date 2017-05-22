import os
import re
from setuptools import setup, find_packages

# reading the package version without loading the package.
with open(os.path.join(os.path.dirname(__file__), 'yml2pdf', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

dependencies = [
    'PyYAML',
    'reportlab'
]


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="yml2pdf",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid.mardani@gmail.com",
    description="Generates PDF from YAML1 using ReportLab",
    maintainer="Vahid Mardani",
    maintainer_email="vahid.mardani@gmail.com",
    packages=find_packages(),
    platforms=["any"],
    install_requires=dependencies,
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries'
    ],
)
