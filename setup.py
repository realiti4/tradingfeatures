from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tradingfeatures",
    version="0.6.2",
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
    packages=find_packages(),
    install_requires=["numpy", "pandas", "requests", "tqdm"],
)
