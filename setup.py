from setuptools import find_packages, setup

VERSION = '0.2.1'

setup(
    name='simiotics-s3',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'boto3',
        'simiotics',
    ],
    description='Simiotics S3 integration',
    author='Neeraj Kashyap',
    author_email='neeraj@simiotics.com',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Version Control',
    ],
    url='https://github.com/simiotics/simiotics-s3',
    entry_points={
        'console_scripts': [
            'simiotics_s3 = simiotics_s3.cli:main'
        ]
    }
)
