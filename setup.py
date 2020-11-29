from setuptools import setup, find_packages

setup(
    name='her_name_is_alice',
    version='0.0.1',
    author='Borodin Gregory',
    author_email='grihabor@gmail.com',
    install_requires=[
        'click',
        'pandas',
        'matplotlib',
    ],
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['alice=her_name_is_alice.main:main'],
    }
)