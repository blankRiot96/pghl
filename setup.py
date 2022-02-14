from setuptools import setup, find_packages

# py -m pip install --upgrade build
# py -m build
# twine upload dist/*
VERSION = "0.0.1"
DESCRIPTION = "A PyGame Helper Library, a support library for pygame applications."
LONG_DESCRIPTION = """
A PyGame Helper Library, a support library for pygame applications.
It contains support for tasks such as animation, sprite sheets and projectiles to name a 
few, and also contains some code obtained from various other projects of mine, written not specifically
for this library, but used multiple times throughout my pygame journey.
"""

# Setup
setup(
    name="pghl",
    version=VERSION,
    author="Axis (blankRiot96)",
    email="blankRiot96@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pygame"],
    python_requires=">=3.10",
    keywords=["pygame", "game library", "game toolkit"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: pygame",
        "Topic :: Games/Entertainment"
        "Intended Audience :: Developers"
    ],
)


