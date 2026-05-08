#!/usr/bin/env python3
"""
Setup configuration for pip package
Enables: pip install human-flourishing-frameworks
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="human-flourishing-frameworks",
    version="1.0.0",
    author="Human Flourishing Frameworks Community",
    author_email="board@human-flourishing-frameworks.org",
    description="Open-source system for detecting and fixing unfair AI systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/human-flourishing-frameworks/human-flourishing-frameworks",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "hff=app:main",
            "hff-node=app:run",
            "hff-update=auto_updater:check_for_updates",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Tracker": "https://github.com/human-flourishing-frameworks/human-flourishing-frameworks/issues",
        "Documentation": "https://github.com/human-flourishing-frameworks/human-flourishing-frameworks/tree/master/docs",
        "Source Code": "https://github.com/human-flourishing-frameworks/human-flourishing-frameworks",
    },
)
