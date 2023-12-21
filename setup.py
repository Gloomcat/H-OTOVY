import re
from pathlib import Path
from setuptools import setup, find_packages


def load_version():
    """ Loads a version file content """
    filename = Path(__file__).resolve().parent / \
        "assistant" / "__init__.py"
    with open(filename, "rt") as version_file:
        conan_init = version_file.read()
        version = re.search(
            r"__version__ = '([0-9.]+)'", conan_init).group(1)
        return version


setup(
    name="assistant",
    version=load_version(),
    description="Contacts and notes management solution with CLI by H-OTOVY team",
    url="https://github.com/Gloomcat/H-OTOVY",
    python_requires=">=3.7, <4",
    packages=find_packages(),
    install_requires=["rich"],
    entry_points={
        "console_scripts": [
            "personal-assistant=assistant.main:run",
        ],
    },
)
