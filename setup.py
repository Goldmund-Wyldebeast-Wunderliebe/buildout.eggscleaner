# -*- coding: utf-8 -*-
"""
This module contains the tool of buildout.eggscleaner
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1.2'

long_description = (
    read('README.rst')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('buildout', 'eggscleaner', 'eggscleaner.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n')

entry_point = 'buildout.eggscleaner:install'
entry_points = {
        "zc.buildout.extension": ["default= %s" % entry_point]
        }

tests_require = [ 'zc.buildout','zope.testing', 'zc.recipe.egg']

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
      url="https://github.com/thepjot/buildout.eggscleaner",
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['buildout', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='buildout.eggscleaner.tests.test_suite',
      entry_points=entry_points,
      )
