import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aliash",
    version="1.0.0",
    author="dnck",
    author_email="noneya@business.com",
    description="This project is just great!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dnck/aliash",
    packages=setuptools.find_packages(),
    install_requires=[
        "click>=7.1.1",
        "python-dotenv==0.11.0"
    ],
    entry_points="""
        [console_scripts]
        aliash=package.main:CLI
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11.7',
)
