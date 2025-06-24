from setuptools import setup

setup(
    name='RedDotDigitizer',
    version='1.0.0',
    description='Graph digitization GUI tool for extracting data points from images',
    author='Atul Kumar Dubey',
    author_email='atuldubey413@gmail.com',
    py_modules=['red_dot_digitizer'],
    install_requires=[
        'matplotlib',
        'pillow',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'reddotdigitizer=red_dot_digitizer:main',
        ],
    },
)