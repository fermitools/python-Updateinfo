import os
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'updateinfo', 'about.py'), 'r') as f:
    exec(f.read(), about)

setup(
    name='Updateinfo',
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    url=about['__url__'],
    long_description=open('README.txt').read(),

    packages=['updateinfo', 'updateinfo.tests', 'updateinfo.collection', 'updateinfo.collection.store', 'updateinfo.helpers', 'updateinfo.package', 'updateinfo.package.store', 'updateinfo.reference', 'updateinfo.reference.store', 'updateinfo.update', 'updateinfo.updateinfo'],

    test_suite='updateinfo.tests',
    requires=[
        'PyYAML',
        'json',
    ],
    classifiers=[
        'Programming Language :: Python',
    ],
)
