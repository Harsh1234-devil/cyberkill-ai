from setuptools import setup, find_packages

setup(
    name="cyberkill",
    version="1.0.0",
    author="Harsh Vardhan",
    author_email="harsh@cyberkill.ai",
    description="Next-Generation Autonomous Multi-Agent Cybersecurity Platform & MCP Server",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "pydantic>=2.0.0",
        "click>=8.1.0",
        "rich>=13.4.0",
    ],
    entry_points={
        "console_scripts": [
            "cyberkill=cyberkill.cli:main",
        ],
    },
)
