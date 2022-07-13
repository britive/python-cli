from setuptools import setup
from src.version import __version__


setup(
    name='pybritive',
    version=__version__,
    py_modules=['pybritive'],
    url='https://github.com/britive/python-cli',
    python_requires='>=3.7, <4',
    install_requires=[
        'click',
        'requests',
        'PyYAML',
        'merge_args',
        'tabulate',
        'toml',
        'britive @ https://github.com/britive/python-sdk/releases/download/v2.6.0/britive-2.6.0.tar.gz#egg=britive-2.6.0'
    ],
    entry_points={
        'console_scripts': [
            'pybritive = pybritive:safe_cli'
        ]
    }
)
