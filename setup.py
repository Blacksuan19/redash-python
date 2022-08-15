from setuptools import find_packages, setup

requirements = [
    "requests",
]
setup(
    name="redash-python",
    version="0.0.2",
    author="Abubakar Yagoub",
    author_email="i@blacksuan19.dev",
    description="A more complete Python client for the Redash API",
    packages=find_packages(),
    requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
