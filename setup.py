__author__ = 'Paul Severance'

from setuptools import setup

setup(
    name='fire-api',
    version='0.0.1',
    author='Paul Severance',
    author_email='paul.severance@gmail.com',
    url='https://github.com/sugarush/fire-api',
    packages=[
        'fire_api'
    ],
    description='A JSONAPI implementation.',
    install_requires=[
        'fire_document@git+https://github.com/sugarush/fire-document@master#egg=fire-document',
        'fire_router@git+https://github.com/sugarush/fire-router@master#egg=fire-router',
        'fire_asynctest@git+https://github.com/sugarush/fire-asynctest@master#egg=fire-asynctest',
        'fire_odm@git+https://github.com/sugarush/fire-odm@master#egg=fire-odm'
    ]
)
