"""Setup."""
from setuptools import setup, find_packages

setup(
    name="crypto",
    version="0.1.0",
    packages=find_packages(),
    scripts=[
        './crypto/bin/crypto'
    ],
    install_requires=[
        "pandas",
        "requests"
    ],
    author="Melchior Prugniaud",
    author_email="melchior.prugniaud@gmail.com",
    include_package_data=True)
