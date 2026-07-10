from setuptools import setup

setup(
    name='itpp',
    version='1.0.0',
    description='Interpreter per il linguaggio I++',
    py_modules=['main'],
    packages=['itpp'],
    entry_points={'console_scripts': ['itpp=main:main']},
)
