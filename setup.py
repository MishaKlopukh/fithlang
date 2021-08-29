from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='fithlang',
    version='0.1',
    description='The Fith programming language',
    long_description=readme(),
    url='http://github.com/mishaklopukh/fithlang',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Compilers',
    ],
    author='Misha Klopukh',
    author_email='mklopukh2019@fau.edu',
    license='MIT',
    packages=['fith'],
    entry_points = {
        'console_scripts': [
            '5cc=fith.fith:main',
            'fithc=fith.fith:main',
            '5asm=fith.asm5:main',
            '5vm=fith.vm5:main'
        ],
    },
    include_package_data=True,
    zip_safe=False
)
