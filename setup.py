"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['shotput/Shotput.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'shotput.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleName': 'Shotput',
        'CFBundleDisplayName': 'Shotput',
        'CFBundleGetInfoString': "Upload screenshots to an SFTP server!",
        'CFBundleIdentifier': "com.amussey.osx.shotput",
        'CFBundleVersion': "1.1.0",
        'CFBundleShortVersionString': "1.1.0",
        'NSHumanReadableCopyright': u"Copyright © 2018, Andrew Mussey, All Rights Reserved."
    },
    'packages': [
        'rumps',
        'argh',
        'asn1crypto',
        'bcrypt',
        'cffi',
        'cryptography',
        'idna',
        'paramiko',
        'pathtools',
        'pyasn1',
        'pycparser',
        'nacl',  # 'PyNaCl',
        'objc',  # pyobjc-core
        'AppKit',  # pyobjc-framework-Cocoa
        'Cocoa',  # pyobjc-framework-Cocoa
        'CoreFoundation',  # pyobjc-framework-Cocoa
        'Foundation',  # pyobjc-framework-Cocoa
        'pyperclip',
        'dateutil',  # 'python-dateutil',
        'yaml',  # PyYAML
        'watchdog',
    ],
}


setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    packages=['shotput'],
    setup_requires=['py2app'],
    # dependency_links=['http://github.com/justin-pierce/rumps/tarball/master#egg=rumps']
)
