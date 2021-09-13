from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements.txt", "r", encoding="utf-8") as file:
    requirements = file.read()

setup(
    name="rvdl",
    version="1.0.0",
    author="Oliver Roy Knox",
    author_email="dev@oliverroyknox.com",
    license="MIT",
    description="A video download tool for Reddit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="github.com/oliverroyknox/rvdl",
    py_modules=["rvdl", "controllers", "exceptions", "strategies"],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires=">=3.9",
    entry_points= '''
        [console_scripts]
        rvdl=rvdl:start
    '''
)