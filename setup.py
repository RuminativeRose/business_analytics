'''
Setup.py
'''
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

extras_require={
}

long_description_spec=open('README.md', 'r', encoding='utf-8').read()

entry_points={
    'console_scripts': [
        'main=main:main']
    }
try:
    packages=find_packages(exclude='tests*')
except:
    packages=[]
    
# standard options: https://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers=[
    'Development Status :: 3 - Alpha'
    "Programming Language :: Python :: 3 :: Only",
    "Operating System :: OS Independent"
    ]
keywords=["finance","llm"]

config = {'name': 'BusinessAnalyticsRose',
    'version': '0.1.0',
    'description': 'A Demonstrative LLM-Assisted Business Analytics/Finance Tool',
    'long_description': long_description_spec,
    'author': 'Rose N.',
    'url': 'https://github.com/RuminativeRose/business_analytics',
    'download_url': 'https://pypi.python.org/pypi/BusinessAnalyticsRose',
    'author_email': 'rose.nestor@gmail.com',
    'packages': packages,
    'include_package_data':True,
    'entry_points': entry_points,
    'license': 'Apache-2.0',
    'keywords': keywords,
    'classifiers': classifiers,
    }

setup(**config)
