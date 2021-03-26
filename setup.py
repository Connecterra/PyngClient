from setuptools import setup, find_packages

package_name = "pyngclient"

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests", "isodate"]

setup(
    name=package_name,
    packages=[package_name],
    setup_requires=["setuptools-git-versioning"],
    version_config={
        "starting_version": "0.0.2",
        "dirty_template": "{tag}",
    },
    license="GPLv3",
    description="PyngClient to MonitoringService",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Connecterra B.V. (Igor Schouten)",
    author_email="igors@connecterra.io",
    url="https://github.com/Connecterra/PyngClient",
    keywords=["Monitoring"],
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
