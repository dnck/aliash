import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aliash_tool", # Replace with your own username
    version="1.0.0",
    author="dnck",
    author_email="noneya@business.com",
    description="This project is just great!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://project_url.com/git",
    packages=setuptools.find_packages(),
    # include_package_data=True,
    install_requires=[
        "click>=7.1.1",
        "python-dotenv==0.11.0"
    ],
    entry_points="""
        [console_scripts]
        aliash=aliash_tool.main:CLI
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11.7',
)
