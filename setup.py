#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from setuptools import setup, find_packages, Command
from setuptools.command.install import install
from setuptools.command.develop import develop
from sys import platform as _platform
from shutil import rmtree
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
NAME = 'labelImg'
REQUIRES_PYTHON = '>=3.0.0'
REQUIRED_DEP = ['pyqt5', 'lxml']
about = {}

with open(os.path.join(here, 'libs', '__init__.py')) as f:
    exec(f.read(), about)

with open("README.rst", "rb") as readme_file:
    readme = readme_file.read().decode("UTF-8")

with open("HISTORY.rst", "rb") as history_file:
    history = history_file.read().decode("UTF-8")

# OS specific settings
SET_REQUIRES = ['setuptools>=64', 'wheel']
if _platform == "linux" or _platform == "linux2":
   # linux
   print('linux')
elif _platform == "darwin":
   # MAC OS X
   SET_REQUIRES.append('py2app')

required_packages = find_packages(include=['labelImg', 'libs', 'labelImg.*'])
required_packages.append('labelImg')

APP = [NAME + '.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'resources/icons/app.icns'
}


def compile_resources():
    print("Compiling resources")
    try:
        # Run the first pyrcc5 command in the root directory
        subprocess.check_call(['pyrcc5', 'resources.qrc', '-o', 'resources.py'], cwd=here)

        # Run the second pyrcc5 command in the libs directory
        libs_dir = os.path.join(here, 'libs')
        subprocess.check_call(['pyrcc5', '../resources.qrc', '-o', 'resources.py'], cwd=libs_dir)
    except subprocess.CalledProcessError:
        print("Error: Failed to compile Qt resources. Ensure pyrcc5 is installed.")


class CustomInstallCommand(install):
    """Custom install command to run resource compilation."""
    def run(self):
        print("Running custom install command")
        compile_resources()
        install.run(self)


class CustomDevelopCommand(develop):
    """Custom develop command to run resource compilation in editable installs."""
    def run(self):
        print("Running custom develop command")
        compile_resources()
        develop.run(self)


class UploadCommand(Command):
    """Support setup.py upload."""

    description=readme + '\n\n' + history,

    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            self.status('Fail to remove previous builds..')
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag -d v{0}'.format(about['__version__']))
        os.system('git tag v{0}'.format(about['__version__']))
        # os.system('git push --tags')

        sys.exit()


# Define setup options
setup_options = {
    'name': NAME,
    'version': about['__version__'],
    'description': "LabelImg is a graphical image annotation tool and label object bounding boxes in images",
    'long_description': readme + '\n\n' + history,
    'author': "TzuTa Lin",
    'author_email': 'tzu.ta.lin@gmail.com',
    'url': 'https://github.com/tzutalin/labelImg',
    'python_requires': REQUIRES_PYTHON,
    'package_dir': {'labelImg': '.'},
    'packages': required_packages,
    'entry_points': {
        'console_scripts': [
            'labelImg=labelImg.labelImg:main'
        ]
    },
    'include_package_data': True,
    'install_requires': REQUIRED_DEP,
    'license': "MIT license",
    'zip_safe': False,
    'keywords': 'labelImg labelTool development annotation deeplearning',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    'package_data': {'data/predefined_classes.txt': ['data/predefined_classes.txt']},
    'setup_requires': SET_REQUIRES,
    'cmdclass': {
        'build_resources': CompileResources,
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'upload': UploadCommand,
    }
}

# Conditionally add 'app' only for py2app
if 'py2app' in sys.argv:
    setup_options['app'] = APP
    setup_options['options'] = {'py2app': OPTIONS}

# Call setup with setup_options
setup(**setup_options)
