from setuptools import setup


setup(
    name='trender',
    version='0.1',
    py_modules=['trender'],
    install_requires=[
        'Click',
        'jinja2',
        'pytest',
    ],
    entry_points='''
        [console_scripts]
        trender=trender:main
    ''',
)
