import setuptools

setuptools.setup(
    name="sayuDB",
    version="0.0.1",
    author="Arsybai",
    description="Database management system based on python and JSON.",
    packages=["sayuDB"],
    license="MIT",
    author_email="me@arsybai.com",
    url="https://github.com/Arsybai/sayuDB",
    keywords=[
        'database',
    ],
    install_requires=[
    'requests',
    'tabulate',
    'flask'
    ],
    readme="README.md"
)