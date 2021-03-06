# this file contains some placeholders
# that are changed in a local copy if a release is made

import setuptools

README = 'README.md'  # the path to your readme file
README_MIME = 'text/markdown'  # it's mime type

with open(README, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mebispy",
    version="<>",  # placeholder (tag of release)
    author="leonhma",
    description="python bindings for mebis",
    url="https://github.com/leonhma/mebispy",
    long_description=long_description,
    long_description_content_type=README_MIME,
    packages=setuptools.find_packages(),
    author_email="leonhardmasche@gmail.com",  # the email of the repo owner
    classifiers=[  # add some info about you package
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'requests'
    ]
)
