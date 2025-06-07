from setuptools import setup, find_packages

setup(
    name='risingwave-mcp',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A RisingWave MCP project using fastmcp and risingwave-py',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'fastmcp',
        'risingwave-py',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
