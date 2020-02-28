import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitfinexget",
    version="0.1",
    author="Onur Cetinkol",
    author_email="author@example.com",
    description="A small package to get history, easily download all avaliable history to csv or update current csv files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/realiti4/bitfinexget",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=["bitfinexget"],
    install_requires=["pandas", "requests"],
)