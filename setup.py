
from os import path
from setuptools import setup, find_packages 

def setup_package():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

    metadata = dict(
        name='data_preparation',
        version="1.0.0",
        description="Utilities package for Artificial "
                    "Intelligence",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Pyth-Men-Code/data-prep-package.git",
        python_requires='>=3.11.0',
        packages=find_packages(
            exclude=("")),
        install_requires=[
            'numpy == 1.26.2',
            'matplotlib == 3.8.4',
            'scikit_learn == 1.4.2',
            'pandas == 2.2.2'

        ]
    )
    setup(**metadata, include_package_data=True)





if __name__ == '__main__':
  setup_package()

