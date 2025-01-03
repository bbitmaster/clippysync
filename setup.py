from setuptools import setup, find_packages

setup(
    name='clippysync',
    version='2.0.0-rc0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'iroh==0.29.0',
        'clipman',
    ],
    entry_points={
        'console_scripts': [
            'clippysync=clippysync.main:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool for syncing clipboards across multiple machines',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/clippysync',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)