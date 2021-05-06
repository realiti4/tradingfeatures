from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tradingfeatures",
    version="0.6.4",
    author="Onur Cetinkol",
    author_email="realiti44@gmail.com",
    description="A useful tool to download market history from popular exchanges.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/realiti4/tradingfeatures",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords="download market history binance bitfinex bitmex bitstamp",
    packages=find_packages(
        exclude=["test", "test.*", "examples", "examples.*", "docs", "docs.*"]
    ),
    install_requires=["numpy", "pandas", "requests", "tqdm"],
)
