from setuptools import find_packages, setup

setup(
    name='ss-rando-bot',
    description='racetime.gg bot for generating SS Randomizer seeds.',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    url='https://racetime.gg/lozssr',
    project_urls={
        'Source': 'https://github.com/floha258/ss-rando-bot',
    },
    version='1.0.0',
    install_requires=[
        'racetime_bot@git+git://github.com/racetimeGG/racetime-bot@tww-rando-bot',
        'PyGithub>=1.53'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'randobot=randobot:main',
        ],
    },
)