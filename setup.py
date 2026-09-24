from setuptools import setup, find_packages
from os import path
from pybit import VERSION as __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pybit',
    version=__version__,
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
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Framework :: AsyncIO",
    ],
    keywords="bybit api connector",
    packages=find_packages(exclude=("tests", "tests.*", "examples", "examples.*")),
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.22.0",
        "websocket-client>=1.5.0",
        "pycryptodome>=3.20.0",
    ],
    extras_require={
        # Async HTTP + WebSocket surface. Import guards under
        # ``pybit.asyncio.__init__`` raise an informative ImportError with the
        # ``pip install pybit[async]`` hint if either dependency is missing.
        # 3.10.11 is the first aiohttp release without CVE-2024-23334 /
        # CVE-2024-27306 / CVE-2024-52304.
        "async": ["aiohttp>=3.10.11,<4", "websockets>=12,<16"],
        # Proxy support for AsyncWebsocketManager (uses websockets_proxy).
        "proxy": ["websockets_proxy>=0.1.3,<1"],
    },
)
