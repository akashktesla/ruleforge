from setuptools import setup
from Cython.Build import cythonize


setup(
name="ruleforge",
version="0.0.1",
packages=["ruleforge"],
ext_modules=cythonize([], language_level=3),
)
