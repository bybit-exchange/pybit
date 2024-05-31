from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pybit',
    version='5.6.1',
    description='Python3 Bybit HTTP/WebSocket API Connector', 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bybit-exchange/pybit",
    license="MIT License",
    author="Dexter Dickinson",
    author_email="dexter.dickinson@bybit.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="bybit api connector",
    packages=["pybit", "pybit.legacy"],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "websocket-client",
        "websockets",
    ],
)
