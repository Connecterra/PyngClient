from setuptools import setup, find_packages

package_name = "ctra-ping-client"

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests", "isodate"]

setup(
    name=package_name,
    packages=[package_name],
    version="0.0.1",
    license="GPLv3",
    description="Connecterra GenericPing Client",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Connecterra (Igor Schouten)",
    author_email="igors@connecterra.io",
    url="https://github.com/Connecterra/PyngClient",
    keywords=["Connecterra"],
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",  # Options: "3 - Alpha", "4 - Beta", "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
