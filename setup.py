from importlib.metadata import entry_points
from setuptools import find_packages
from setuptools import setup

setup(
   name='aytemplar',
   version='1.0.0',
   description='aytemplar makes all files templates',
   author='Aypahyo',
   author_email='Aypahyo@github.com',
   url='https://github.com/Aypahyo/ayTempler',
   packages=['aytemplar_core'],
   py_modules=['aytemplar'],
   entry_points={
    'console_scripts' : [
      'aytemplar = aytemplar:main'
    ],
   }
)


















