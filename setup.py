"""Package file for `pockette`."""

from setuptools import setup, find_packages

from pockette import VERSION


with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='pockette',
    package=['pockette'],
    version=VERSION,
    author='Thomas Thoren',
    license='MIT',
    url='https://github.com/ThomasThoren/pockette',
    description='Command line tools for working with Pocket',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords=['Pocket', 'CLI'],
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    python_requires='>=3.7.0',
    install_requires=[
        'click~=8.1',
        'requests~=2.24'
    ],
    extras_require={
        'dev': [
            'coverage~=7.4',
            'mypy~=1.8',
            'pylint~=3.0',
            'pytest~=8.0',
            'pytest-cov~=4.1',
            'types-requests~=2.24',
            'types-setuptools'
        ]
    },
    entry_points={
        'console_scripts': [
            'pockette=pockette.cli:cli'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
