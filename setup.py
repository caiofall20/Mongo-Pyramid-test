from setuptools import setup
requires = [
    'pyramid',
    'pyramid_chameleon',
    'waitress',
    'pymongo',
]
setup(
    name='PyMovie',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = PyMovie:main'
        ],
    }
)
