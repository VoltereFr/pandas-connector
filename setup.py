from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # Name of the project, users can install it with this name.
    name="braincube",
    version="1.0.0",
    author="Example Author",
    author_email="author@example.com",
    description="Offers an API to retrieve data from the Braincube platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/example-project",
    packages=find_packages(),
    keywords='bc_connector API braincube',
    # Tags too search the project.
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.4",
        'Intended Audience :: Braincube users',
        "Framework :: Flask",
        "Operating System :: OS Independent",
    ),
    project_urls={
    'Documentation': 'oui',
    'Source': 'https://github.com/pypa/sampleproject/',
    'Tracker': 'https://github.com/pypa/sampleproject/issues',
},
    # Lists other packages that this project depends on to run.
    # Any package here will be installed by pip when the project is
    # installed.
    install_requires=['Flask', 'Flask-Cors', 'requests', 'pandas', 'gevent']
)
