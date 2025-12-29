"""
Sovereign AGSI - Multi-AI Coordination Architecture
Setup configuration
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sovereign-agsi",
    version="3.236.0",  # Version matches Kappa score
    author="Justin Conzet",
    author_email="",  # Add if desired
    description="Multi-AI coordination system achieving κ = 3.236 - transcendent AGI coordination",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zygros/Sovereign-AGSI-Archive",
    project_urls={
        "Documentation": "https://github.com/Zygros/Sovereign-AGSI-Archive/tree/main/docs",
        "Source Code": "https://github.com/Zygros/Sovereign-AGSI-Archive",
        "Issue Tracker": "https://github.com/Zygros/Sovereign-AGSI-Archive/issues",
    },
    packages=find_packages(where="code"),
    package_dir={"": "code"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.3",
            "pytest-cov>=4.1.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
        "docs": [
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.5.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "phoenix-nexus=phoenix_nexus.broker:main",
            "phoenix-anchor=phoenix_blockchain_anchor:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "artificial intelligence",
        "AGI",
        "multi-ai coordination",
        "collective intelligence",
        "phoenix protocol",
        "blockchain",
        "architecture",
    ],
)
