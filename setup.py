from setuptools import setup, find_packages

setup(
    name='naukri-auto-apply',
    version='0.1.0',
    description='Automated job application system for Naukri.com',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/your-repo/naukri-auto-apply',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'selenium==4.18.1',
        'webdriver-manager==4.0.2',
        'schedule==1.2.2',
        'python-dotenv==1.0.1',
        'pyyaml==6.0.2',
    ],
    extras_require={
        'dev': [
            'pytest==8.3.3',
            'pytest-cov==5.0.0',
            'flake8==7.1.1',
        ],
    },
    entry_points={
        'console_scripts': [
            'naukri-auto-apply=naukri_auto_apply.main:main',
        ],
    },
    python_requires='>=3.8',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
