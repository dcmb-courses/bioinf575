from setuptools import setup

setup(name='demo_pkg',
      version='0.1.0',
      packages=['demo_pkg'],
      entry_points={
          'console_scripts': [
              'test_run = demo_pkg.test:main', 
              'another_module_run = demo_pkg.another_module:main',
              'test_say_hi = demo_pkg.test:say_hi'
          ]
      },
      )