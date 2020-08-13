import setuptools

setuptools.setup(
    name="uq-ecp", # Replace with your own username
    version="0.0.1",
    author="Richal Verma",
    author_email="richalverma00@gmail.com",
    description="A package to scrape UQ's course profiles",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "bs4",
        "lxml"
    ]
)