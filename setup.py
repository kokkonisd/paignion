import setuptools

from paignion.definitions import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paignion",
    version=__version__,
    author="Dimitri Kokkonis",
    author_email="kokkonisd@gmail.com",
    description="A simple game engine for adventure text games.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kokkonisd/paignion",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["pyyaml", "markdown", "pymdown-extensions"],
    package_data={"paignion": ["frontend/*"]},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "paignion = paignion.__main__:paignion_main_function",
        ],
    },
    python_requires=">=3.6",
)
