from setuptools import setup, find_packages

setup(
    name='smeftjet',
    version='0.1.0',
    description='library for smeft_jet project related computation',
    author='Mark N. Costantini',
    author_email='mnc33@cam.ac.uk',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
)

