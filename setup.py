from setuptools import setup

setup(
    name='bca_web',
    version='1.0',
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask',
                      'mysqlclient',
                      'flask_mysqldb',
                      'flask_login',
                      'python-ldap']
    )