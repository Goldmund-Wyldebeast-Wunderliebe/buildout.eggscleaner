# -*- coding: utf-8 -*-
"""
This module contains the tool of buildout.eggscleaner
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1.6dev'

long_description = (
    read('README.rst')
    + '\n' +
    'Detailed Documentation\n'
    '======================\n'
    + '\n' +
    read('src', 'buildout', 'eggscleaner', 'eggscleaner.txt')
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n')

setup(name='buildout.eggscleaner',
      version=version,
      description="A buildout extension to move non-used eggs to a specified directory",
      long_description=long_description,
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='buildout extensions eggs directory clean',
      author='Peter Uittenbroek',
      author_email='uittenbroek@goldmund-wyldebeast-wunderliebe.com',
      url="https://github.com/Goldmund-Wyldebeast-Wunderliebe/buildout.eggscleaner",
      license='ZPL',
      packages = find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['buildout', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        ],
      extras_require={
          'test': [
              'zc.buildout',
              'zope.testing', 
              'zc.recipe.egg'
          ]
      },
      # test_suite='buildout.eggscleaner.tests.test_suite',
      entry_points={
        "zc.buildout.extension": ["default= buildout.eggscleaner:install"]
        },
      )
