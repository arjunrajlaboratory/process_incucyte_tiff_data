from setuptools import setup, find_packages

setup(
    name='process_incucyte_tiff_data',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'process-incucyte-tiff-data=process_incucyte_tiff_data.process_tiff_data:main',
        ],
    },
    install_requires=[
        'tifffile',  # Add 'tifffile' to the list of required packages
        'imagecodecs', # Add 'imagecodecs' to the list of required packages
        # You can specify versions as well, e.g., 'tifffile>=2021.7.2', 'imagecodecs>=2021.6.8'
        # Add any other required packages here, each as a string in this list
    ],
    # Include any other parameters you had before or may want to add
)
