import os

from setuptools import setup, find_packages


classifiers = """\
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Topic :: Internet :: WWW/HTTP
Operating System :: Unix
"""

def read(*rel_names):
    return open(os.path.join(os.path.dirname(__file__), *rel_names)).read()


setup(
    name='httpcode',
    version='0.6',
    url='http://github.com/rspivak/httpcode',
    license='MIT',
    description='httpcode - explain HTTP status code',
    author='Ruslan Spivak',
    author_email='ruslan.spivak@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['colorama'],
    zip_safe=False,
    entry_points="""\
    [console_scripts]
    hc = httpcode:main
    """,
    classifiers=filter(None, classifiers.split('\n')),
    long_description=read('README.rst') + '\n\n' + read('CHANGES.rst'),
    extras_require={'test': []}
    )
