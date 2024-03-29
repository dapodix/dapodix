from setuptools import setup

setup(
    name='dapodix',
    version='0.2.0',
    description='Alat bantu aplikasi Dapodik',
    author='Habib Rohman',
    author_email="hexatester@protonmail.com",
    url='https://github.com/hexatester/dapodix',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["dapodix"],
    install_requires=[
        'python',
        'openpyxl',
        'dapodik',
    ],
    entry_points={
        'console_scripts': [
            'dapodix=dapodix.__main__:main'
        ]
    }
)
