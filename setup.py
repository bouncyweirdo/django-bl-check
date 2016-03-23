import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-bl-check',
    version='0.1.16',
    packages=[
        'blacklist_check',
        'blacklist_check.management',
        'blacklist_check.management.commands',
        'blacklist_check.migrations',
    ],
    include_package_data=True,
    install_requires=['dnspython3', 'celery[redis]'],
    license='BSD (3-Clause) License',
    description='A Django app that checks if IPs are accessible and/or if are blacklisted.',
    long_description=README,
    url='https://gitlab.com/valentin87/django-blacklist-check',
    author='Valentin Olaru',
    author_email='valentin.olaru26@gmail.com',
)
