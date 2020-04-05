from distutils.core import setup
import py2exe

setup(name='ksm_debugger',
      version='0.1.0',
      packages=['my_project'],
      entry_points={
          'console_scripts': [
              'my_project = my_project.__main__.main'
          ]
      },
      )