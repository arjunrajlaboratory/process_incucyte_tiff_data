from setuptools import setup, find_packages

setup(
    name='process_incucyte_tiff_data',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'process-incucyte-tiff-data = process_incucyte_tiff_data.process_tiff_data:main',
        ],
    },
)
