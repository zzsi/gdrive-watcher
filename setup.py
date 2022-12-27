from setuptools import setup

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("README.md") as f:
    long_description = f.read()

setup(
    name="gbt",
    version="0.1",
    description="A gradient boosted tree library with minimal coding required.",
    url="https://github.com/zzsi/gbt",
    author="Zhangzhang Si",
    author_email="zhangzhang.si@gmail.com",
    license="MIT",
    packages=["gbt"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
)
