import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='lizzy',
    version='1.0.1',
    author='Sarah Schmoller',
    description='Python implementation of the Eliza chatbot',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sarah-schmoller/lizzy',
    license='MIT',
    packages=['lizzy'],
    package_data={'lizzy': ['./mirror.json', './script.json', './synonyms.json']},
    include_package_data=True,
    install_requires=['regex']
)
