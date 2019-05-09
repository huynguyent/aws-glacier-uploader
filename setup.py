import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-glacier-tool",
    version="1.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['glacier=glacier.glacier:main']
    },
    install_requires=['docpie', 'boto3']
)
