import setuptools


DEPENDENCIES = ["pygame>=2.0.0"]


with open("README.md", "r") as file:
    FULL_DESC = file.read()


setuptools.setup(
    name="pygame-ui-toolkit",
    author="Ben Edwards",
    version="1.0.3",
    description="A package for creating UI elements in pygame",
    long_description=FULL_DESC,
    long_description_content_type="text/markdown",
    url="https://github.com/Ben-Edwards44/pygame-ui-toolkit",
    packages=setuptools.find_packages(exclude=["examples"]),
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