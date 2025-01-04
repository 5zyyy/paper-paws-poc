from setuptools import setup, find_packages

setup(
    name="paper-paws",
    version="1.0.0",
    description="Paper trading for meme coins",
    author="awl",
    package_dir={"": "src"},
    packages=find_packages(where="src"), 
    install_requires=[
        "pandas==2.2.3",
        "streamlit==1.41.1",
        "pyyaml==6.0.2",
        "streamlit-extras==0.5.0",
        "duckdb==1.1.3",
    ],
    python_requires=">=3.6",
)