from setuptools import setup
from version import __version__

setup(
    name='PyBritive',
    version=__version__,
    py_modules=['pybritive'],
    install_requires=[
        'Click'
    ],
    entry_points={
        'console_scripts': [
            'pybritive = pybritive:cli'
        ]
    }
)
