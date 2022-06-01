from setuptools import setup, find_packages



with open("README.md") as f:
    long_description = f.read()

install_requires = [
        "antlr4-python3-runtime==4.7.2"
        ]
setup(
    name="ottrToSmwPython",
    version=0.1,
    description="SMW plugin parsing OTTR in Semantic Media Wiki.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'OtterParserExtension':'includes/ottrToSmwPython'},
    packages=['includes/ottrToSmwPython','includes/ottrToSmwPython/stOTTR'],
    python_requires=">=3.8",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "ottrToSMW = includes.ottrToSmwPython.printOttrInSmw:run"
        ]
    }
)

