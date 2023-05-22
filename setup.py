"""Package file for `pockette`."""

from setuptools import setup, find_packages  # type: ignore

from pockette import VERSION


with open('README.md', 'r') as f:
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
    packages=find_packages(exclude=('tests')),
    include_package_data=True,
    python_requires='>=3.7.0',
    install_requires=[
        'click==7.1.2',
        'requests==2.31.0'
    ],
    extras_require={
        'dev': [
            'coverage==5.1',
            'mypy==0.780',
            'pylint==2.5.3',
            'pytest==5.4.3',
            'pytest-cov==2.10.0'
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
