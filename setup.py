from setuptools import setup

setup(
    name="UforaFileFetcher",
    version="0.1",
    packages=["uff"],
    entry_points={
        "console_scripts": ['uforafilefetcher=uff.uforafilefetcher:run'],
    }, install_requires=[
        "requests",
        "beautifulsoup4",
        "tqdm",
        "inquirer",
        "pathvalidate"
    ]
)
