import setuptools
from setuptools import setup
from setuptools import find_packages

setup(
    name='Contacts',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/Jake-Sheehan/Contacts',
    license='MIT',
    author='Jake Sheehan',
    author_email='jake.sheehan.dev@gmail.com',
    description='This is a cloud based contacts storage app',
    install_requires=['tk', 'pymongo', 'pymongo[srv]'],
    python_requires='>=3'
)
