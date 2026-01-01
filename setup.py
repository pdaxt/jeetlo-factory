from setuptools import setup, find_packages

setup(
    name="jeetlo-factory",
    version="1.0.0",
    description="Enforced content creation pipeline for JeetLo",
    author="JeetLo",
    author_email="pran@jeetlo.ai",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        # No external dependencies for core functionality
        # TTS and video tools are system dependencies
    ],
    entry_points={
        "console_scripts": [
            "jeetlo-validate=jeetlo_factory.ci:main",
        ],
    },
)
