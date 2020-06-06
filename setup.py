from setuptools import setup

# Read in the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='swr_ed',
    version='0.0.1',
    install_requires=requirements,
    author='Luis Visintini',
    author_email='lvisintini@gmail.com',
    packages=['swr_ed', ],
    url='https://github.com/lvisintini/SWRebellionEditor',
    license='GNU GENERAL PUBLIC LICENSE',
    description='A library with tools that let you edit data files for the Star Wars Rebellion video game (1998)',
)