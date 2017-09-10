#from distutils.core import setup
from setuptools import setup
setup(name='todos',
      version='0.1',
      packages=['src', 'src.parser', 'src.plugins'],
      entry_points={
          'console_scripts': [
              'todos = src.todos:main',
          ],
      },
      install_requires=[
          'requests',
          'toml'
      ])
