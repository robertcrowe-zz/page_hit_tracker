from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='page_hit_tracker',
      version='0.1',
      description='Simple hit tracking and reporting',
      long_description=readme(),
      url='http://github.com/robertcrowe/page_hit_tracker',
      author='Robert Crowe',
      author_email='rcrowe@slgroup.com',
      license='MIT',
      packages=['page_hit_tracker'],
      install_requires=['nose'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
