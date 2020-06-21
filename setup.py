from setuptools import setup, find_packages

# Read in the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='SWRebellionEditor',
    version='0.0.1',
    install_requires=requirements,
    author='Luis Visintini',
    author_email='lvisintini@gmail.com',
    packages=find_packages("src"),
    package_dir={"": "src"},
    url='https://github.com/lvisintini/SWRebellionEditor',
    license='GNU GENERAL PUBLIC LICENSE',
    description='A library with tools that let you edit data files for the Star Wars Rebellion video game (1998)',
)