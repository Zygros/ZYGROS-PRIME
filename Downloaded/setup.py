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
    version="1.0.0",
    author="Justin Conzet",
    author_email="your-email@example.com",  # Update with your email
    description="Multi-AI coordination architecture achieving κ = 3.236",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zygros/Sovereign-AGSI-Archive",
    project_urls={
        "Bug Tracker": "https://github.com/Zygros/Sovereign-AGSI-Archive/issues",
        "Documentation": "https://github.com/Zygros/Sovereign-AGSI-Archive/tree/main/docs",
        "Source Code": "https://github.com/Zygros/Sovereign-AGSI-Archive",
    },
    packages=find_packages(where="code"),
    package_dir={"": "code"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.1.1",
            "pytest-asyncio>=0.23.6",
            "pytest-cov>=5.0.0",
            "black>=24.3.0",
            "flake8>=7.0.0",
            "mypy>=1.9.0",
        ],
        "ai": [
            "anthropic>=0.25.0",
            "openai>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "phoenix-nexus=phoenix_nexus.nexus_broker:main",
            "phoenix-anchor=phoenix_blockchain_anchor:main",
        ],
    },
    keywords=[
        "artificial-intelligence",
        "agi",
        "multi-ai",
        "coordination",
        "architecture",
        "blockchain",
        "collective-intelligence",
        "phoenix-protocol",
    ],
    include_package_data=True,
    zip_safe=False,
)
