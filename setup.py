"""
Setup
"""
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="plantuml_creator",
    version="1.0.0",
    description="Library to generate plantuml code from python objects",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Eitol/plantuml_creator",
    author="Hector Oliveros",
    author_email="hector.oliveros.leon@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["plantuml_creator"],
    include_package_data=True,
    install_requires=[
        "attrs==19.3.0",
        "importlib-metadata==1.3.0",
        "more-itertools==8.0.2"
        "packaging==20.0",
        "pluggy==0.13.1",
        "py==1.8.1",
        "pyparsing==2.4.6",
        "pytest==5.3.2",
        "six==1.13.0",
        "str2bool==1.1",
        "stringcase==1.2.0",
        "wcwidth==0.1.8",
        "zipp==0.6.0",
    ],
    entry_points={
        "console_scripts": []
    },
)
