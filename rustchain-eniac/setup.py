#!/usr/bin/env python3
"""
ENIAC RustChain Miner - Setup Script
=====================================
Installation: pip install -e .
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rustchain-eniac-miner',
    version='1.0.0',
    author='RustChain ENIAC Team',
    author_email='eniac@rustchain.org',
    description='RustChain miner for ENIAC (1945) - LEGENDARY Tier',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RustChainFX/rustchain-eniac',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Historical Reconstruction',
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests>=2.28.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'eniac-miner=simulator.eniac_miner:main',
            'eniac-fingerprint=hardware.fingerprint:main',
        ],
    },
    keywords='rustchain blockchain mining eniac vintage hardware proof-of-antiquity',
    project_urls={
        'Bug Reports': 'https://github.com/RustChainFX/bounties/issues/388',
        'Source': 'https://github.com/RustChainFX/rustchain-eniac',
        'Documentation': 'https://github.com/RustChainFX/rustchain-eniac#readme',
    },
)
