import setuptools  # type: ignore

version = {}
with open("mutwo/reaper_version/__init__.py") as fp:
    exec(fp.read(), version)

VERSION = version["VERSION"]


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

extras_require = {"testing": ["pytest>=7.1.1"]}

setuptools.setup(
    name="mutwo.reaper",
    version=VERSION,
    license="GPL",
    description="Reaper extension for event based framework for generative art",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Levin Eric Zimmermann",
    author_email="levin.eric.zimmermann@posteo.eu",
    url="https://github.com/mutwo-org/mutwo.reaper",
    project_urls={"Documentation": "https://mutwo-org.github.io"},
    packages=[
        package
        for package in setuptools.find_namespace_packages(include=["mutwo.*"])
        if package[:5] != "tests"
    ],
    setup_requires=[],
    install_requires=[
        "mutwo.core>=2.0.0, <3.0.0",
    ],
    extras_require=extras_require,
    python_requires=">=3.9, <4",
)
