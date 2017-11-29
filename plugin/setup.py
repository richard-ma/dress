from setuptools import setup

setup(
        name='DressMove-Plugin',
        version='0.0.1',
        py_modules=['dress_plugin'],
        entry_points={'dress': {'dress_plugin = dress_plugin:DressPlugin'}}
)
