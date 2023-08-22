import setuptools


with open("README.md", "r") as file:
    FULL_DESC = file.read()


with open("requirements.txt", "r") as file:
    DEPENDENCIES = file.read().split("\n")


setuptools.setup(
    name="pygame-ui-toolkit",
    author="Ben Edwards",
    version="0.0.1",
    description="A package for creating UI elements in pygame",
    long_description=FULL_DESC,
    long_description_content_type="text/markdown",
    url="https://github.com/Ben-Edwards44/pygame-ui-toolkit",
    py_modules=["src"],
    packages=setuptools.find_packages("src"),
    install_requires=DEPENDENCIES,
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Intended Audience :: Developers"
    ]
)