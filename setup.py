from setuptools import setup

setup(
    name = 'acuity',
    version = '0.0',
    author = 'sugarc0de',
    author_email = 'sugarc0de@localhost',
    zip_safe = False,
    packages = ['acuity', 'twisted.plugins'],
    install_requires = [
        'Twisted', 'jinja2',
    ],
    package_data={'twisted': ['plugins/acuity.py']},
)

