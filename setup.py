import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tradingfeatures",
    version="0.3.12",
    author="Onur Cetinkol",
    author_email="realiti44@gmail.com",
    description="A small package to get history, easily download all avaliable history to csv or update current csv files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/realiti4/tradingfeatures",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=["tradingfeatures"],
    install_requires=["pandas", "requests"],
)
