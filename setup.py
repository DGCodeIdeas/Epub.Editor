from setuptools import setup, find_packages

setup(
    name="epsilon-editor",
    version="2.0.0",
    description="Feature-rich modular EPUB editor optimized for Android Termux with intuitive TUI",
    author="Jules",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "textual",
        "beautifulsoup4",
        "lxml",
    ],
    entry_points={
        "console_scripts": [
            "epsilon-editor=epub_editor_pro.app:main",
            "epsilon-cli=epub_editor_pro.cli:main",
        ],
    },
)
