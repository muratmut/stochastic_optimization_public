from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='stochastic_opt',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    author='Murat Mut',
    author_email='mutmurat2@gmail.com',
    description='2-stage Stochastic optimization model for demand uncertainty'
)
