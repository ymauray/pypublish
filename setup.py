from setuptools import setup, find_packages
from pypublish import version
from pypublish import name

setup(
    name=name(),
    version=version(),
    packages=find_packages('src'),
    url="https://github.com/frenchguy/pypublish",
    maintainer="Yannick Mauray",
    maintainer_email="yannick@frenchguy.ch",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Podcast publishers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.6.8'
    ],
    python_requires='~=3.6',
    entry_points={
        'console_scripts': [
            'pypublish=pypublish:main'
        ]
    }
)
