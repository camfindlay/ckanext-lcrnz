from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name='ckanext-lcrnz',
    version=version,
    description='CKAN extension for the Landcare Research Datastore',
    long_description='''
    ''',
    classifiers=[],
    keywords='',
    author='Open Knowledge',
    author_email='services@okfn.org',
    url='https://github.com/okfn/ckanext-esdstandards',
    license='AGPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.lcrnz'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        lcrnz=ckanext.lcrnz.plugin:NewZealandLandcarePlugin
    ''',
)
