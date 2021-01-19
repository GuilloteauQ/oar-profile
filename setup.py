from setuptools import setup

setup(
    # Application name:
    name="OAR-Profile",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Quentin Guilloteau",
    author_email="Quentin.Guilloteau@inria.fr",

    # Packages
    packages=["app"],

    # Include additional files into the package
    # include_package_data=True,
    entry_points={
        'console_scripts': ['oar-profile=app.main:main'],
    },

    # Details
    url="https://github.com/GuilloteauQ/oar-profile",

    #
    # license="LICENSE.txt",
    description="Runs a Cluster profile with OAR",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
    ]
)
