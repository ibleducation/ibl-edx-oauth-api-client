import os
from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ibl_edx_oauth_api_client',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='Simplify the OAuth2 authorization process between an external service and Open edX',
    long_description=README,
    author='IBL Education',
    author_email='engineering@ibleducation.com',
    install_requires = [
        'django>=1.8',
        'djangorestframework',
        'requests>=2.9.2'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
