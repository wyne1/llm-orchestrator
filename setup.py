from setuptools import setup, find_packages

setup(
    name="llm_wrapper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "requests",
        "openai",
    ],
    description="A unified interface for interacting with various LLM chat models.",
    author="Zeerak",
    author_email="zeerak.wyne@gmail.com",
    url="https://github.com/yourusername/llm_wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)